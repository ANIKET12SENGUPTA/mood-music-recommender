import random

MOOD_GENRES = {
    "happy": ["pop", "dance", "indie-pop"],
    "sad": ["blues", "acoustic", "indie-pop"],
    "calm": ["jazz", "classical", "acoustic"],
    "angry": ["metal", "rock", "alternative"],
    "energetic": ["edm", "dance", "house"],
    "relaxed": ["acoustic", "jazz", "ambient"],
    "neutral": ["pop", "rock", "jazz"],
}

MOOD_KEYWORDS = {
    "happy": ["happy", "joyful", "love", "great", "amazing", "excited", "celebratory", "party", "sunny", "travel", "dance"],
    "sad": ["sad", "lonely", "heartbroken", "depressed", "upset", "down", "crying", "melancholy", "breakup", "rainy"],
    "calm": ["calm", "tired", "sleepy", "lazy", "bored", "study", "focus", "reading", "work"],
    "angry": ["angry", "frustrated", "mad", "furious", "annoyed", "stressed", "rage"],
    "energetic": ["energetic", "excited", "hyped", "pumped", "thrilled", "gym", "workout", "running", "driving", "nightdrive"],
    "relaxed": ["relaxed", "peaceful", "chill", "slow", "rested", "cozy", "rain", "storm", "mellow"],
}

ACTIVITY_GENRES = {
    "gym": ["edm", "hip-hop", "dance"],
    "workout": ["edm", "hip-hop", "rock"],
    "study": ["jazz", "classical", "ambient"],
    "focus": ["jazz", "ambient", "lofi"],
    "rain": ["acoustic", "indie-pop", "jazz"],
    "road": ["rock", "pop", "edm"],
    "drive": ["rock", "pop", "edm"],
    "party": ["dance", "pop", "house"],
    "sleep": ["ambient", "acoustic", "classical"],
}


def get_genres(mood):
    mood = mood.lower().strip()
    genre_pool = MOOD_GENRES.get(mood, MOOD_GENRES["neutral"])
    num_genres = random.randint(2, 3)
    return random.sample(genre_pool, min(num_genres, len(genre_pool)))


def detect_genres(text):
    if not text:
        return get_genres("neutral")

    normalized = text.lower()
    for mood, keywords in MOOD_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return get_genres(mood)

    for activity, genres in ACTIVITY_GENRES.items():
        if activity in normalized:
            return genres[:3]

    for mood in MOOD_GENRES:
        if mood in normalized:
            return get_genres(mood)

    return get_genres("happy")