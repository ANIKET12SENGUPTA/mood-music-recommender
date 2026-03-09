from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.mood_engine import analyze_mood
from app.genre_engine import detect_genres
from app.recommender import get_candidates
from app.ranking import rank_by_embedding
from app.collaborative import boost_by_history

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    text = data.get("text", "").strip()

    if not text:
        return {
            "emotion": "unknown",
            "genres": [],
            "recommendations": []
        }

    emotion, valence, energy = analyze_mood(text)
    genres = detect_genres(text)
    candidates = get_candidates(genres, valence, energy)

    if not candidates:
        return {
            "emotion": emotion,
            "genres": genres,
            "recommendations": []
        }

    ranked = rank_by_embedding(text, candidates)
    final = boost_by_history(ranked)

    recommendations = []

    for t in final[:10]:
        try:
            recommendations.append({
                "name": t["name"],
                "artist": t["artists"][0]["name"],
                "url": t["external_urls"]["spotify"]
            })
        except:
            continue

    return {
        "emotion": emotion,
        "genres": genres,
        "recommendations": recommendations
    }
