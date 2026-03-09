import json
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "data", "user_history.json")


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def boost_by_history(tracks):
    history = load_history()

    if not history:
        random.shuffle(tracks)
        return tracks

    listened_artists = set()

    for t in history:
        artist = t.get("artist")
        if artist:
            listened_artists.add(artist)

    boosted = []
    normal = []

    for t in tracks:
        try:
            artist = t["artists"][0]["name"]

            if artist in listened_artists:
                boosted.append(t)
            else:
                normal.append(t)
        except:
            normal.append(t)

    final = boosted + normal

    try:
        sample = []

        for t in final[:5]:
            sample.append({
                "artist": t["artists"][0]["name"],
                "name": t["name"]
            })

        history.extend(sample)
        save_history(history)

    except:
        pass

    return final
