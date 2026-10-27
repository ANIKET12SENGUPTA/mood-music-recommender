import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "data", "user_history.json")


def _normalize(value):
    return (value or "").strip().lower()


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def boost_by_history(tracks, user_history=None, liked_tracks=None):
    history = user_history if user_history is not None else load_history()
    liked_names = {
        _normalize(item.get("track", {}).get("name") or item.get("name"))
        for item in (liked_tracks or [])
        if item
    }
    history_artists = {_normalize(item.get("artist")) for item in history if item.get("artist")}
    history_tracks = {_normalize(item.get("name")) for item in history if item.get("name")}

    if not history and not liked_tracks:
        return tracks

    scored_tracks = []
    for track in tracks:
        artist = (track.get("artists") or [{}])[0].get("name", "")
        track_name = track.get("name", "")
        artist_key = _normalize(artist)
        track_key = _normalize(track_name)
        score = 0.0

        if artist_key and artist_key in history_artists:
            score += 0.5
        if track_key and track_key in history_tracks:
            score += 0.7
        if track_key and track_key in liked_names:
            score += 0.8

        scored_tracks.append((track, score))

    scored_tracks.sort(key=lambda item: item[1], reverse=True)
    ranked = [track for track, _ in scored_tracks]

    try:
        for item in ranked[:5]:
            artist = (item.get("artists") or [{}])[0].get("name")
            if artist and item.get("name"):
                history.append({"artist": artist, "name": item["name"]})
        save_history(history)
    except (TypeError, ValueError, OSError):
        pass

    return ranked
