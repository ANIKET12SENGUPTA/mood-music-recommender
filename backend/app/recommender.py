import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from app.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)

ALLOWED_GENRES = [
    "pop", "rock", "hip-hop", "dance",
    "edm", "jazz", "classical", "metal",
    "country", "r-n-b", "house", "techno",
    "indie-pop", "indie-rock"
]


def get_candidates(genres, valence, energy):
    filtered = [g for g in genres if g in ALLOWED_GENRES]

    if not filtered:
        filtered = ["pop"]

    query = " OR ".join(filtered[:2])

    try:
        results = sp.search(q=query, type="track", limit=10)
        return results["tracks"]["items"]
    except Exception as e:
        print("Spotify search failed:", e)
        return []
