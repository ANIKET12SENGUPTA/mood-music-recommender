import pytest

from app.genre_engine import detect_genres
from app.mood_engine import analyze_mood
from app.recommender import build_recommendation_payload


def test_analyze_mood_detects_sad_words():
    emotion, valence, energy = analyze_mood("I feel lonely, heartbroken, and exhausted")
    assert emotion == "sad"
    assert 0.0 <= valence <= 1.0
    assert 0.0 <= energy <= 1.0


def test_detect_genres_uses_mood_context():
    genres = detect_genres("I am furious and angry")
    assert genres
    assert any(genre in genres for genre in ["rock", "metal"])


def test_build_recommendation_payload_includes_metadata():
    payload = build_recommendation_payload(
        text="I am happy and energetic",
        genres=["pop", "dance"],
        liked_tracks=[{"name": "Good as Hell", "artists": [{"name": "Lizzo"}], "album": {"name": "Cuz I Love You"}}],
        user_history=[{"artist": "Lizzo", "name": "Good as Hell"}],
    )
    assert payload["emotion"] == "happy"
    assert payload["genres"]
    assert payload["personalized"] is True
    assert payload["score_breakdown"]["history_boost"] >= 0


def test_analyze_mood_handles_mixed_natural_language():
    emotion, valence, energy = analyze_mood("I need a rainy-day vibe, low energy, cozy and relaxed, but still a bit upbeat")
    assert emotion in {"relaxed", "calm", "happy"}
    assert 0.0 <= valence <= 1.0
    assert 0.0 <= energy <= 1.0


def test_detect_genres_handles_activity_and_mood_mix():
    genres = detect_genres("I want hype gym music for a late-night drive with a strong beat")
    assert genres
    assert any(genre in genres for genre in ["dance", "edm", "rock", "pop"])
