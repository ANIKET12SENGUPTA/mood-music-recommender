from __future__ import annotations

from app.collaborative import load_history
from app.genre_engine import detect_genres
from app.mood_engine import analyze_mood
from app.spotify_client import search_tracks_for_genres

ALLOWED_GENRES = [
    "pop", "rock", "hip-hop", "dance",
    "edm", "jazz", "classical", "metal",
    "country", "r-n-b", "house", "techno",
    "indie-pop", "indie-rock", "blues", "acoustic",
    "ambient", "alternative"
]


def build_recommendation_payload(text, genres=None, liked_tracks=None, user_history=None):
    emotion, valence, energy = analyze_mood(text)
    mood_genres = genres or detect_genres(text)
    filtered_genres = [genre for genre in mood_genres if genre in ALLOWED_GENRES]
    if not filtered_genres:
        filtered_genres = ["pop"]

    history = user_history if user_history is not None else load_history()
    personalized = bool(liked_tracks or history)
    breakdown = {
        "mood_signal": round((valence + energy) / 2, 3),
        "history_boost": round(min(0.35, max(0.0, len(history) / 25)), 3),
        "liked_track_boost": round(min(0.25, max(0.0, len(liked_tracks or []) / 20)), 3),
    }
    total_score = round(sum(breakdown.values()), 3)

    return {
        "emotion": emotion,
        "genres": filtered_genres,
        "personalized": personalized,
        "score_breakdown": {
            **breakdown,
            "total": total_score,
        },
    }


def get_candidates(genres, limit: int = 10):
    filtered = [g for g in genres if g in ALLOWED_GENRES]
    if not filtered:
        filtered = ["pop"]
    try:
        return search_tracks_for_genres(filtered, limit=limit)
    except RuntimeError:
        return []
