import uuid
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.collaborative import boost_by_history, load_history
from app.genre_engine import detect_genres
from app.mood_engine import analyze_mood
from app.ranking import rank_by_embedding
from app.recommender import build_recommendation_payload, get_candidates
from app.spotify_client import (
    build_auth_url,
    clear_session,
    create_playlist_for_user,
    exchange_code_for_tokens,
    get_session,
    get_user_liked_tracks,
    get_user_profile,
    get_user_recent_tracks,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="VibeVault")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _merge_user_history(liked_tracks, recent_tracks, file_history=None):
    history = []
    for item in (file_history or []):
        if isinstance(item, dict):
            history.append(item)
    for item in liked_tracks:
        track = item.get("track") if isinstance(item, dict) and item.get("track") else item
        history.append({
            "artist": (track.get("artists") or [{}])[0].get("name"),
            "name": track.get("name"),
        })
    for item in recent_tracks:
        track = item.get("track") if isinstance(item, dict) and item.get("track") else item
        history.append({
            "artist": (track.get("artists") or [{}])[0].get("name"),
            "name": track.get("name"),
        })
    return history


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    session_id = request.cookies.get("spotify_session_id")
    profile = get_user_profile(session_id) if session_id else None
    return templates.TemplateResponse("index.html", {"request": request, "user": profile})


@app.get("/auth/login")
async def spotify_login(request: Request):
    session_id = request.cookies.get("spotify_session_id") or uuid.uuid4().hex
    try:
        auth_url = build_auth_url(session_id)
    except RuntimeError as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)

    response = RedirectResponse(url=auth_url, status_code=302)
    response.set_cookie(key="spotify_session_id", value=session_id, httponly=True, samesite="lax")
    return response


@app.get("/auth/callback")
async def spotify_callback(request: Request, code: str | None = None, state: str | None = None):
    session_id = request.cookies.get("spotify_session_id")
    if not session_id:
        return JSONResponse({"error": "Spotify session is missing. Please try logging in again."}, status_code=400)

    try:
        exchange_code_for_tokens(code or "", state or "", session_id)
    except (RuntimeError, ValueError) as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="spotify_session_id", value=session_id, httponly=True, samesite="lax")
    return response


@app.get("/auth/logout")
async def spotify_logout(request: Request):
    session_id = request.cookies.get("spotify_session_id")
    clear_session(session_id)
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("spotify_session_id")
    return response


@app.get("/auth/status")
async def auth_status(request: Request):
    session_id = request.cookies.get("spotify_session_id")
    profile = get_user_profile(session_id) if session_id else None
    return {"logged_in": bool(profile), "user": profile}


@app.post("/playlist/create")
async def create_playlist(request: Request):
    data = await request.json()
    session_id = request.cookies.get("spotify_session_id")
    track_uris = data.get("track_uris") or []
    name = data.get("name") or "VibeVault Mix"

    try:
        result = create_playlist_for_user(session_id, name, track_uris)
        return {"success": True, "playlist": result}
    except RuntimeError as exc:
        return JSONResponse({"error": str(exc)}, status_code=401)
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)


@app.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    text = (data.get("text") or "").strip()
    session_id = request.cookies.get("spotify_session_id")

    if not text:
        return {"emotion": "unknown", "genres": [], "recommendations": [], "logged_in": bool(get_session(session_id))}

    try:
        liked_tracks = get_user_liked_tracks(session_id, limit=20)
        recent_tracks = get_user_recent_tracks(session_id, limit=20)
        history = _merge_user_history(liked_tracks, recent_tracks, load_history())
        emotion, _, _ = analyze_mood(text)
        genres = detect_genres(text)
        payload = build_recommendation_payload(
            text=text,
            genres=genres,
            liked_tracks=liked_tracks,
            user_history=history,
        )
        candidates = get_candidates(genres, limit=12)

        if not candidates:
            return {
                "emotion": emotion,
                "genres": payload["genres"],
                "recommendations": [],
                "personalized": payload["personalized"],
                "score_breakdown": payload["score_breakdown"],
                "logged_in": bool(get_session(session_id)),
            }

        ranked = rank_by_embedding(text, candidates, user_history=history, liked_tracks=liked_tracks)
        final = boost_by_history(ranked, user_history=history, liked_tracks=liked_tracks)

        recommendations = []
        for track in final[:10]:
            try:
                artist = (track.get("artists") or [{}])[0].get("name", "Unknown Artist")
                recommendations.append({
                    "name": track.get("name", "Unknown Title"),
                    "artist": artist,
                    "url": (track.get("external_urls") or {}).get("spotify", ""),
                    "uri": track.get("uri", ""),
                })
            except Exception:
                continue

        return {
            "emotion": emotion,
            "genres": payload["genres"],
            "recommendations": recommendations,
            "personalized": payload["personalized"],
            "score_breakdown": payload["score_breakdown"],
            "logged_in": bool(get_session(session_id)),
        }
    except Exception as exc:
        return {
            "emotion": "error",
            "genres": [],
            "recommendations": [],
            "message": str(exc),
            "logged_in": bool(get_session(session_id)),
        }