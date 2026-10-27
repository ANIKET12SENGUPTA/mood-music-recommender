import re

from sklearn.metrics.pairwise import cosine_similarity

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None

_model = None


def get_model():
    global _model
    if _model is None and SentenceTransformer is not None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _heuristic_rank(user_text, tracks, user_history=None, liked_tracks=None):
    if not tracks:
        return []

    normalized_text = re.findall(r"[a-z0-9]+", (user_text or "").lower())
    history_keywords = set()
    for item in (user_history or []):
        history_keywords.update(re.findall(r"[a-z0-9]+", str(item.get("name", "") + " " + str(item.get("artist", "")).lower())))
    liked_keywords = set()
    for item in (liked_tracks or []):
        track_name = (
            item.get("track", {}).get("name") if isinstance(item, dict) and item.get("track") else item.get("name", "")
        )
        liked_keywords.update(re.findall(r"[a-z0-9]+", str(track_name).lower()))

    ranked = []
    for track in tracks:
        name = (track.get("name") or "").lower()
        artist = ((track.get("artists") or [{}])[0].get("name") or "").lower()
        track_text = f"{name} {artist}"
        score = 0.0
        for token in normalized_text:
            if token in track_text:
                score += 0.12
        if history_keywords and any(word in track_text for word in history_keywords):
            score += 0.35
        if liked_keywords and any(word in track_text for word in liked_keywords):
            score += 0.45
        ranked.append((track, score))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return [track for track, _ in ranked]


def rank_by_embedding(user_text, tracks, user_history=None, liked_tracks=None):
    if not tracks:
        return []

    try:
        model = get_model()
        if model is None:
            raise RuntimeError("SentenceTransformer model unavailable")

        user_vec = model.encode([user_text])
        song_texts = []
        for track in tracks:
            name = track.get("name", "")
            artist = "Unknown"
            if track.get("artists"):
                artist = track["artists"][0]["name"]
            song_texts.append((f"{name} {artist}")[:200])

        song_vecs = model.encode(song_texts)
        scores = cosine_similarity(user_vec, song_vecs)[0]
        ranked = sorted(zip(tracks, scores), key=lambda item: item[1], reverse=True)
        return [entry[0] for entry in ranked]
    except Exception:
        return _heuristic_rank(user_text, tracks, user_history=user_history, liked_tracks=liked_tracks)