import random
import re
from collections import Counter

MOOD_FEATURES = {
    "happy": {"valence": 0.9, "energy": 0.8},
    "sad": {"valence": 0.2, "energy": 0.3},
    "calm": {"valence": 0.5, "energy": 0.2},
    "angry": {"valence": 0.3, "energy": 0.9},
    "energetic": {"valence": 0.8, "energy": 0.9},
    "relaxed": {"valence": 0.6, "energy": 0.3},
    "neutral": {"valence": 0.55, "energy": 0.55},
}

MOOD_SYNONYMS = {
    "excited": "energetic",
    "thrilled": "energetic",
    "hyped": "energetic",
    "pumped": "energetic",
    "party": "happy",
    "celebrate": "happy",
    "celebration": "happy",
    "tired": "calm",
    "sleepy": "calm",
    "bored": "calm",
    "lazy": "calm",
    "lonely": "sad",
    "heartbroken": "sad",
    "depressed": "sad",
    "upset": "sad",
    "down": "sad",
    "crying": "sad",
    "romantic": "happy",
    "love": "happy",
    "great": "happy",
    "amazing": "happy",
    "awesome": "happy",
    "good": "happy",
    "joyful": "happy",
    "frustrated": "angry",
    "annoyed": "angry",
    "mad": "angry",
    "furious": "angry",
    "rage": "angry",
    "stressed": "angry",
    "anxious": "sad",
    "chill": "relaxed",
    "peaceful": "relaxed",
    "cozy": "relaxed",
    "rainy": "relaxed",
    "stormy": "relaxed",
    "focus": "calm",
    "studying": "calm",
    "study": "calm",
    "workout": "energetic",
    "gym": "energetic",
    "driving": "energetic",
    "roadtrip": "energetic",
    "travel": "happy",
    "nightdrive": "energetic",
    "late-night": "energetic",
    "melancholy": "sad",
    "mellow": "relaxed",
    "sunset": "happy",
    "sunny": "happy",
    "breakup": "sad",
    "weird": "neutral",
}

ACTIVITY_CONTEXT = {
    "workout": "energetic",
    "gym": "energetic",
    "run": "energetic",
    "running": "energetic",
    "work": "calm",
    "study": "calm",
    "focus": "calm",
    "reading": "relaxed",
    "sleep": "relaxed",
    "rest": "relaxed",
    "party": "happy",
    "club": "happy",
    "dance": "happy",
    "driving": "energetic",
    "trip": "happy",
    "road": "energetic",
    "rain": "relaxed",
    "storm": "relaxed",
    "sad": "sad",
    "angry": "angry",
    "depressed": "sad",
    "broke": "sad",
    "love": "happy",
    "romance": "happy",
}


def _normalize_words(raw_text):
    text = str(raw_text or "").lower()
    words = re.findall(r"[a-z0-9-]+", text)
    return words


def analyze_mood(mood_input):
    if not mood_input or not str(mood_input).strip():
        return "neutral", 0.5, 0.5

    words = _normalize_words(mood_input)
    detected_features = []
    detected_emotions = []
    for word in words:
        mapped = MOOD_SYNONYMS.get(word)
        if word in MOOD_FEATURES:
            detected_features.append(MOOD_FEATURES[word])
            detected_emotions.append(word)
        elif mapped in MOOD_FEATURES:
            detected_features.append(MOOD_FEATURES[mapped])
            detected_emotions.append(mapped)

    for word in words:
        mapped_context = ACTIVITY_CONTEXT.get(word)
        if mapped_context and mapped_context in MOOD_FEATURES:
            detected_features.append(MOOD_FEATURES[mapped_context])
            detected_emotions.append(mapped_context)

    if detected_features:
        avg_valence = sum(feature["valence"] for feature in detected_features) / len(detected_features)
        avg_energy = sum(feature["energy"] for feature in detected_features) / len(detected_features)
        emotion = Counter(detected_emotions).most_common(1)[0][0]
        return emotion, round(avg_valence, 3), round(avg_energy, 3)

    return "neutral", round(random.uniform(0.4, 0.7), 3), round(random.uniform(0.4, 0.7), 3)