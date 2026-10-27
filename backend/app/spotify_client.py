from __future__ import annotations

import threading
import time
from typing import Any

import spotipy
from spotipy import Spotify
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from app.config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SCOPES,
    SESSION_TTL_SECONDS,
)

_SESSION_STORE: dict[str, dict[str, Any]] = {}
_SESSION_LOCK = threading.Lock()


def _now() -> int:
    return int(time.time())


def _require_app_credentials() -> None:
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise RuntimeError("Spotify credentials are missing. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your environment or .env file.")


def get_app_client() -> Spotify | None:
    try:
        _require_app_credentials()
    except RuntimeError:
        return None

    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def build_auth_url(session_id: str) -> str:
    _require_app_credentials()
    oauth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES,
        open_browser=False,
    )
    auth_url = oauth_manager.get_authorize_url()
    with _SESSION_LOCK:
        _SESSION_STORE[session_id] = {
            "auth_state": oauth_manager.state,
            "created_at": _now(),
            "expires_at": _now() + SESSION_TTL_SECONDS,
        }
    return auth_url


def exchange_code_for_tokens(code: str, state: str, session_id: str) -> dict[str, Any]:
    _require_app_credentials()
    with _SESSION_LOCK:
        session = _SESSION_STORE.get(session_id)
        if not session:
            raise ValueError("Spotify session expired or is missing.")
        if session.get("auth_state") != state:
            raise ValueError("Spotify auth state mismatch.")

    oauth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES,
        open_browser=False,
    )
    token = oauth_manager.get_access_token(code)
    if not token:
        raise RuntimeError("Spotify token exchange failed.")

    with _SESSION_LOCK:
        session = _SESSION_STORE.setdefault(session_id, {"created_at": _now()})
        session.update({
            "auth_state": state,
            "access_token": token.get("access_token"),
            "refresh_token": token.get("refresh_token"),
            "token_type": token.get("token_type", "Bearer"),
            "expires_at": _now() + int(token.get("expires_in", SESSION_TTL_SECONDS)),
            "scope": token.get("scope", SPOTIFY_SCOPES),
        })
    return session


def get_session(session_id: str | None) -> dict[str, Any] | None:
    if not session_id:
        return None
    with _SESSION_LOCK:
        session = _SESSION_STORE.get(session_id)
        if not session:
            return None
        if session.get("expires_at", 0) <= _now():
            _SESSION_STORE.pop(session_id, None)
            return None
        return session.copy()


def get_session_token(session_id: str | None) -> str | None:
    session = get_session(session_id)
    return session.get("access_token") if session else None


def get_user_profile(session_id: str | None) -> dict[str, Any] | None:
    token = get_session_token(session_id)
    if not token:
        return None
    try:
        client = Spotify(auth=token)
        return client.current_user()
    except SpotifyException as exc:
        if exc.http_status == 401:
            clear_session(session_id)
        return None
    except Exception:
        return None


def get_user_liked_tracks(session_id: str | None, limit: int = 20) -> list[dict[str, Any]]:
    token = get_session_token(session_id)
    if not token:
        return []
    try:
        client = Spotify(auth=token)
        response = client.current_user_saved_tracks(limit=limit)
        return response.get("items", [])
    except SpotifyException as exc:
        if exc.http_status == 401:
            clear_session(session_id)
        return []
    except Exception:
        return []


def get_user_recent_tracks(session_id: str | None, limit: int = 20) -> list[dict[str, Any]]:
    token = get_session_token(session_id)
    if not token:
        return []
    try:
        client = Spotify(auth=token)
        response = client.current_user_recently_played(limit=limit)
        return response.get("items", [])
    except SpotifyException as exc:
        if exc.http_status == 401:
            clear_session(session_id)
        return []
    except Exception:
        return []


FALLBACK_TRACKS = {
    "pop": [
        {"name": "Levitating", "artists": [{"name": "Dua Lipa"}], "external_urls": {"spotify": "https://open.spotify.com/track/390OjegD5ZxXOhgKkxD9J1"}, "uri": "spotify:track:390OjegD5ZxXOhgKkxD9J1"},
        {"name": "Good as Hell", "artists": [{"name": "Lizzo"}], "external_urls": {"spotify": "https://open.spotify.com/track/3Yh9lZc7Lk1a0zX8oU4P9b"}, "uri": "spotify:track:3Yh9lZc7Lk1a0zX8oU4P9b"},
        {"name": "Flowers", "artists": [{"name": "Miley Cyrus"}], "external_urls": {"spotify": "https://open.spotify.com/track/0yLdNVVh1v9o0d2tIhZ1cR"}, "uri": "spotify:track:0yLdNVVh1v9o0d2tIhZ1cR"},
    ],
    "dance": [
        {"name": "Don’t Start Now", "artists": [{"name": "Dua Lipa"}], "external_urls": {"spotify": "https://open.spotify.com/track/3PfIrDoz19wz7qK7tYeuGG"}, "uri": "spotify:track:3PfIrDoz19wz7qK7tYeuGG"},
        {"name": "Titanium", "artists": [{"name": "David Guetta"}], "external_urls": {"spotify": "https://open.spotify.com/track/7gHn1fTXXmTgftfDLeuP3O"}, "uri": "spotify:track:7gHn1fTXXmTgftfDLeuP3O"},
        {"name": "On The Floor", "artists": [{"name": "Jennifer Lopez"}], "external_urls": {"spotify": "https://open.spotify.com/track/4aQDO5C7vUmkzXQ1fUByV3"}, "uri": "spotify:track:4aQDO5C7vUmkzXQ1fUByV3"},
    ],
    "rock": [
        {"name": "Believer", "artists": [{"name": "Imagine Dragons"}], "external_urls": {"spotify": "https://open.spotify.com/track/0pqnGHJpmpxKIB5K8Y1h7M"}, "uri": "spotify:track:0pqnGHJpmpxKIB5K8Y1h7M"},
        {"name": "Thunderstruck", "artists": [{"name": "AC/DC"}], "external_urls": {"spotify": "https://open.spotify.com/track/57bgtoPSgt236HzfBOd8kj"}, "uri": "spotify:track:57bgtoPSgt236HzfBOd8kj"},
        {"name": "The Pretender", "artists": [{"name": "Foo Fighters"}], "external_urls": {"spotify": "https://open.spotify.com/track/7x8dCjCr0x6x2lXK4jM2gA"}, "uri": "spotify:track:7x8dCjCr0x6x2lXK4jM2gA"},
    ],
    "jazz": [
        {"name": "So What", "artists": [{"name": "Miles Davis"}], "external_urls": {"spotify": "https://open.spotify.com/track/4M8nF1m4LzB0Wv4f1r7t0P"}, "uri": "spotify:track:4M8nF1m4LzB0Wv4f1r7t0P"},
        {"name": "Take Five", "artists": [{"name": "Dave Brubeck"}], "external_urls": {"spotify": "https://open.spotify.com/track/1Qq0tS9P9WmU4lU9N0Q4hZ"}, "uri": "spotify:track:1Qq0tS9P9WmU4lU9N0Q4hZ"},
        {"name": "Autumn Leaves", "artists": [{"name": "Etta Jones"}], "external_urls": {"spotify": "https://open.spotify.com/track/3b5d9w0bbsN3kM0cQ4F5H2"}, "uri": "spotify:track:3b5d9w0bbsN3kM0cQ4F5H2"},
    ],
    "classical": [
        {"name": "Clair de Lune", "artists": [{"name": "Claude Debussy"}], "external_urls": {"spotify": "https://open.spotify.com/track/4QhZb5vYCOjRcnw11Jb6Ct"}, "uri": "spotify:track:4QhZb5vYCOjRcnw11Jb6Ct"},
        {"name": "Für Elise", "artists": [{"name": "Ludwig van Beethoven"}], "external_urls": {"spotify": "https://open.spotify.com/track/5eZ4D0X0M15A8h1mQ5mVg5"}, "uri": "spotify:track:5eZ4D0X0M15A8h1mQ5mVg5"},
        {"name": "Moonlight Sonata", "artists": [{"name": "Ludwig van Beethoven"}], "external_urls": {"spotify": "https://open.spotify.com/track/7uBjMRlHsa1kFQ1R8vP7VO"}, "uri": "spotify:track:7uBjMRlHsa1kFQ1R8vP7VO"},
    ],
    "edm": [
        {"name": "Turn Down for What", "artists": [{"name": "DJ Snake & Lil Jon"}], "external_urls": {"spotify": "https://open.spotify.com/track/67awxiNHNyjaWMY8KJgVwH"}, "uri": "spotify:track:67awxiNHNyjaWMY8KJgVwH"},
        {"name": "Animals", "artists": [{"name": "Martin Garrix"}], "external_urls": {"spotify": "https://open.spotify.com/track/1b9O2Rk5hGv7tvY2d3L1hZ"}, "uri": "spotify:track:1b9O2Rk5hGv7tvY2d3L1hZ"},
        {"name": "Titanium", "artists": [{"name": "David Guetta"}], "external_urls": {"spotify": "https://open.spotify.com/track/7gHn1fTXXmTgftfDLeuP3O"}, "uri": "spotify:track:7gHn1fTXXmTgftfDLeuP3O"},
    ],
    "default": [
        {"name": "Sunflower", "artists": [{"name": "Post Malone"}], "external_urls": {"spotify": "https://open.spotify.com/track/3KkXRkHbMCARz0aVfEt68P"}, "uri": "spotify:track:3KkXRkHbMCARz0aVfEt68P"},
        {"name": "Here Comes the Sun", "artists": [{"name": "The Beatles"}], "external_urls": {"spotify": "https://open.spotify.com/track/45hO9Hm4mxH1IOI2Y9DhkM"}, "uri": "spotify:track:45hO9Hm4mxH1IOI2Y9DhkM"},
        {"name": "Dreams", "artists": [{"name": "Fleetwood Mac"}], "external_urls": {"spotify": "https://open.spotify.com/track/0ofHAoxe9vBkTCp2UQIavz"}, "uri": "spotify:track:0ofHAoxe9vBkTCp2UQIavz"},
    ],
}


def _fallback_tracks_for_genres(genres: list[str], limit: int = 12) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for genre in genres[:3]:
        tracks = FALLBACK_TRACKS.get(genre, FALLBACK_TRACKS["default"])
        selected.extend(tracks)
    if not selected:
        selected.extend(FALLBACK_TRACKS["default"])
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for track in selected:
        key = track.get("name", "").lower()
        if key not in seen:
            deduped.append(track)
            seen.add(key)
    return deduped[:limit]


def search_tracks_for_genres(genres: list[str], limit: int = 12) -> list[dict[str, Any]]:
    filtered = [g for g in genres if g]
    if not filtered:
        filtered = ["pop"]

    client = get_app_client()
    if client is None:
        return _fallback_tracks_for_genres(filtered, limit=limit)

    query = " OR ".join(filtered[:2])
    try:
        results = client.search(q=query, type="track", limit=limit)
        items = results.get("tracks", {}).get("items", [])
        if items:
            return items
        return _fallback_tracks_for_genres(filtered, limit=limit)
    except SpotifyException as exc:
        if exc.http_status == 429:
            return _fallback_tracks_for_genres(filtered, limit=limit)
        return _fallback_tracks_for_genres(filtered, limit=limit)
    except Exception:  # pragma: no cover
        return _fallback_tracks_for_genres(filtered, limit=limit)


def create_playlist_for_user(session_id: str | None, name: str, track_uris: list[str]) -> dict[str, Any]:
    token = get_session_token(session_id)
    if not token:
        raise RuntimeError("Please log in to Spotify before creating a playlist.")
    if not track_uris:
        raise RuntimeError("No songs were selected to add to the playlist.")

    client = Spotify(auth=token)
    profile = client.current_user()
    playlist = client.user_playlist_create(
        profile["id"],
        name or "VibeVault Mix",
        public=False,
        description="Generated by the VibeVault Mood Music Recommender",
    )
    client.playlist_add_items(playlist["id"], track_uris[:100])
    return {
        "id": playlist["id"],
        "name": playlist["name"],
        "url": playlist["external_urls"]["spotify"],
        "track_count": len(track_uris),
    }


def clear_session(session_id: str | None) -> None:
    if not session_id:
        return
    with _SESSION_LOCK:
        _SESSION_STORE.pop(session_id, None)
