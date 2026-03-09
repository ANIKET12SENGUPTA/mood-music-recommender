import random

# Mood → audio feature mapping
MOOD_FEATURES = {
    "happy": {"valence": 0.9, "energy": 0.8},
    "sad": {"valence": 0.2, "energy": 0.3},
    "calm": {"valence": 0.5, "energy": 0.2},
    "angry": {"valence": 0.3, "energy": 0.9},
    "energetic": {"valence": 0.8, "energy": 0.9},
    "relaxed": {"valence": 0.6, "energy": 0.3}
}

# Synonyms mapping
MOOD_SYNONYMS = {

    "excited": "energetic",
    "thrilled": "energetic",
    "hyped": "energetic",
    "pumped": "energetic",

    "tired": "calm",
    "sleepy": "calm",
    "bored": "calm",
    "lazy": "calm",

    "lonely": "sad",
    "heartbroken": "sad",
    "depressed": "sad",
    "upset": "sad",
    "down": "sad",

    "romantic": "happy",
    "love": "happy",
    "great": "happy",
    "amazing": "happy",
    "awesome": "happy",
    "good": "happy",

    "frustrated": "angry",
    "annoyed": "angry",
    "mad": "angry",
    "furious": "angry"
}


def analyze_mood(mood_input):

    if not mood_input:
        return "neutral", 0.5, 0.5

    mood_input = mood_input.lower().strip()
    words = mood_input.split()

    detected_features = []
    detected_emotions = []

    for word in words:

        # Direct mood match
        if word in MOOD_FEATURES:
            detected_features.append(MOOD_FEATURES[word])
            detected_emotions.append(word)

        # Synonym match
        elif word in MOOD_SYNONYMS:
            mapped = MOOD_SYNONYMS[word]
            detected_features.append(MOOD_FEATURES[mapped])
            detected_emotions.append(mapped)

    if detected_features:

        avg_valence = sum(f["valence"] for f in detected_features) / len(detected_features)
        avg_energy = sum(f["energy"] for f in detected_features) / len(detected_features)

        emotion = max(set(detected_emotions), key=detected_emotions.count)

        return emotion, avg_valence, avg_energy

    return "neutral", random.uniform(0.4, 0.7), random.uniform(0.4, 0.7)