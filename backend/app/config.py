import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

HOST = (os.getenv("HOST", "127.0.0.1") or "127.0.0.1").strip()
PORT = int((os.getenv("PORT", "8000") or "8000").strip())

SPOTIFY_CLIENT_ID = (os.getenv("SPOTIFY_CLIENT_ID", "") or "").strip()
SPOTIFY_CLIENT_SECRET = (os.getenv("SPOTIFY_CLIENT_SECRET", "") or "").strip()
SPOTIFY_REDIRECT_URI = (os.getenv("SPOTIFY_REDIRECT_URI", f"http://{HOST}:{PORT}/auth/callback") or "").strip()
SPOTIFY_SCOPES = (
    "user-read-email user-library-read user-top-read "
    "user-read-recently-played playlist-modify-public playlist-modify-private"
)
SESSION_TTL_SECONDS = int((os.getenv("SESSION_TTL_SECONDS", "3600") or "3600").strip())