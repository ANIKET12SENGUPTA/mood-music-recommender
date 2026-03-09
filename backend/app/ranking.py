from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_by_embedding(user_text, tracks):

    if not tracks:
        return []

    user_vec = model.encode([user_text])

    song_texts = []

    for track in tracks:

        name = track.get("name", "")

        artist = "Unknown"
        if track.get("artists"):
            artist = track["artists"][0]["name"]

        song_texts.append((name + " " + artist)[:200])

    song_vecs = model.encode(song_texts)

    scores = cosine_similarity(user_vec, song_vecs)[0]

    ranked = sorted(
        zip(tracks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [r[0] for r in ranked]