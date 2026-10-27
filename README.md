# VibeVault

VibeVault is a mood-based music recommendation app that suggests songs based on the user's emotional state, context, and listening style. It combines lightweight text analysis with Spotify-aware personalization so people can discover tracks that match how they feel.

## Features

- Mood detection from natural-language input such as “happy morning workout” or “sad rain playlist”
- Genre inference from mood and activity context
- Spotify-powered personalization for liked songs and recent plays
- Playlist creation support for saved recommendations
- Clean web interface with personalized login status and recommendation flow
- Graceful fallback recommendations when Spotify is unavailable or rate-limited

## Tech stack

- FastAPI for the backend API
- Jinja2 templates and static frontend assets for the UI
- Spotipy for Spotify OAuth and library access
- Sentence-transformers and lightweight ranking logic for recommendation relevance
- Python 3.11.x for the project runtime

## Project structure

- backend/app: application logic, API routes, and recommendation engine
- backend/data: local user-history storage
- backend/static: frontend CSS and JavaScript
- backend/templates: HTML templates
- backend/tests: regression tests
- backend/run_server.py: startup helper that avoids port conflicts

## Setup

1. Open a terminal in the project root.
2. Create and activate a virtual environment if needed.
3. Install dependencies:

   pip install -r backend/requirements.txt

4. Copy the example environment file and fill in your Spotify credentials:

   copy backend\.env.example backend\.env

5. Update the values in backend/.env with your Spotify client ID, client secret, and redirect URI.

## Run

From the backend folder:

   py -3.11 run_server.py

This launcher checks for a free local port and starts the app reliably without the earlier port conflict issues.

## Spotify login behavior

- Basic recommendations work without Spotify login.
- Logging in unlocks personalization based on liked tracks and recent listening history.
- Users can save generated recommendations to a Spotify playlist after login.

## Environment variables

The app uses these values from backend/.env:

- SPOTIFY_CLIENT_ID
- SPOTIFY_CLIENT_SECRET
- SPOTIFY_REDIRECT_URI
- HOST
- PORT
- SESSION_TTL_SECONDS

## Notes

The project is configured for Python 3.11.x compatibility and is designed to remain usable even if Spotify is temporarily unavailable.