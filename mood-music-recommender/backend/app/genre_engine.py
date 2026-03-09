import random

MOOD_GENRES = {
    "happy": ["pop", "dance", "indie-pop"],
    "sad": ["blues", "acoustic"],
    "calm": ["jazz", "classical"],
    "angry": ["metal", "rock"],
    "energetic": ["edm", "dance", "house"],
    "relaxed": ["acoustic", "jazz"]
}


def get_genres(mood):

    mood = mood.lower().strip()

    genre_pool = MOOD_GENRES.get(mood)

    if not genre_pool:
        genre_pool = [
            "pop",
            "rock",
            "hip-hop",
            "dance",
            "jazz"
        ]

    num_genres = random.randint(2, 3)
    selected_genres = random.sample(genre_pool, min(num_genres, len(genre_pool)))

    return selected_genres


# This is the function main.py expects
def detect_genres(text):

    text = text.lower()

    for mood in MOOD_GENRES:
        if mood in text:
            return get_genres(mood)

    return get_genres("happy")