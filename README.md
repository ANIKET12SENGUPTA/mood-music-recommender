# 🎵 Mood Music Recommender

A mood-aware music recommendation web application built with **FastAPI**, **Spotify API**, **Sentence Transformers**, and a lightweight frontend using **HTML**, **CSS**, and **JavaScript**.

This project takes a user's mood or emotional text input, detects the underlying emotion, maps it to relevant music genres, retrieves candidate songs from Spotify, ranks them using semantic similarity, and applies lightweight personalization using previous listening history.

It is designed as a modular backend-focused project that demonstrates recommendation system design, NLP-inspired text understanding, API integration, ranking logic, and frontend-backend communication in a clean and extensible architecture.

---

## 📌 Overview

Music recommendations are often more meaningful when they reflect how a user feels in the moment. This project aims to simulate a mood-driven recommendation system by combining emotion detection, genre mapping, Spotify-based retrieval, semantic ranking, and simple history-based reordering into a single pipeline.

Instead of asking users to search by artist or song name, the application accepts natural mood descriptions such as:

- `I feel calm and relaxed tonight`
- `I am heartbroken`
- `I am excited and full of energy`
- `I want something happy and fun`

Based on that text, the system generates music recommendations that better align with the user's emotional context.

This project is a strong portfolio project for students and beginner-to-intermediate developers because it showcases practical backend development, modular Python code organization, recommendation logic, and API usage in one complete application.

---

## 🚀 Features

- Accepts free-text mood input from the user
- Detects mood using direct emotion words and synonym matching
- Estimates mood-related audio signals such as valence and energy
- Maps emotions to suitable music genres
- Fetches candidate tracks from Spotify
- Ranks songs using sentence embeddings and cosine similarity
- Applies lightweight personalization using local listening history
- Provides a simple browser-based interface
- Uses FastAPI for backend routing and template rendering
- Organizes code into modular, reusable components

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Jinja2

### Recommendation and NLP
- Sentence Transformers
- scikit-learn
- PyTorch

### API Integration
- Spotipy
- Spotify Web API

### Configuration
- python-dotenv

### Frontend
- HTML
- CSS
- JavaScript

---

## 📂 Project Structure

```bash
mood-music-recommender/
└── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config.py
    │   ├── mood_engine.py
    │   ├── genre_engine.py
    │   ├── spotify_client.py
    │   ├── recommender.py
    │   ├── ranking.py
    │   ├── collaborative.py
    │   ├── templates/
    │   │   └── index.html
    │   └── static/
    │       ├── script.js
    │       └── style.css
    │
    ├── data/
    │   └── user_history.json
    │
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    └── .env.example
```
---

## ⚙️ How It Works
1. User Input
- The user enters a mood or emotional sentence in the web interface.
    - Examples:
      - I feel relaxed
      - I am feeling lonely
      - I want energetic music
      - I am excited today

2. Mood Detection
- The backend analyzes the text using the logic in mood_engine.py.
  - This module:
    - checks for direct mood words such as happy, sad, calm, angry, energetic, and relaxed
    - supports synonym mapping such as:
      - excited → energetic
      - heartbroken → sad
      - sleepy → calm
      - frustrated → angry
  - It then estimates:
    - valence → emotional positivity
    - energy → emotional intensity

3. Genre Detection
- The detected mood is passed to genre_engine.py, which maps mood labels to likely music genres.
- Examples:
  - happy → pop, dance, indie-pop
  - calm → jazz, classical
  - angry → metal, rock
  - energetic → edm, dance, house
- If no strong match is found, the system falls back to a default genre set.

4. Candidate Retrieval
- The selected genres are passed into recommender.py, which uses Spotify credentials from config.py to query the Spotify API and retrieve candidate tracks.
- The recommender:
  - filters genres against an allowed list
  - builds a query from selected genres
  - requests track results from Spotify
  - returns a list of candidate songs

5. Semantic Ranking
- The candidate tracks are then ranked in ranking.py.
- This module:
  - loads the all-MiniLM-L6-v2 sentence transformer model
  - converts user mood text into an embedding
  - converts track-related text into embeddings
  - calculates cosine similarity
  - sorts tracks by semantic closeness to the user input
- This makes the recommendation pipeline more meaningful than a simple keyword match.

6. History-Based Boosting
- The ranked songs are passed to collaborative.py, which reads from data/user_history.json.
- This module:
  - loads previously stored recommendation history
  - checks whether artists from current results appear in listening history
  - boosts songs from known artists
  - stores a sample of recommended songs for future sessions
- This creates a lightweight personalization effect without using a database.

7. Response and Display
- The backend returns:
  - detected emotion
  - selected genres
  - top song recommendations
- The frontend JavaScript in script.js sends the user's text to the /recommend endpoint and dynamically renders the results in the browser.
- The UI is styled using style.css, while index.html serves as the main page template.

---

## 🧠 Recommendation Pipeline
- This project uses a hybrid recommendation strategy that combines multiple techniques:
  - Rule-based mood detection for interpreting user emotion
  - Mood-to-genre mapping for narrowing the music domain
  - Spotify retrieval for real song candidates
  - Embedding-based ranking for semantic relevance
  - History-aware boosting for basic personalization
- This layered design makes the project more practical and realistic than a single-method recommendation system.

---

## 📥 Installation
1. Clone the repository
- git clone https://github.com/ANIKET12SENGUPTA/mood-music-recommender.git
- cd mood-music-recommender/backend

2. Install dependencies
- pip install -r requirements.txt

3. Create the environment file
- Create a .env file inside the backend/ folder and add your Spotify credentials:
  - SPOTIFY_CLIENT_ID=your_spotify_client_id
  - SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
- You can use .env.example as a reference.

---

## ▶️ Run the Application
- From inside the backend/ folder, start the FastAPI server:
  - uvicorn app.main:app --reload
- Then open:
  - http://127.0.0.1:8000

---

<img width="864" height="595" alt="image" src="https://github.com/user-attachments/assets/9ff8c66f-b971-43c7-980b-19bbeb8fefb3" />

---

## 🧪 Skills Demonstrated
- FastAPI application development
- REST API design
- Spotify API integration
- Environment variable management
- Sentence-transformer embeddings
- Cosine similarity ranking
- Rule-based NLP logic
- Modular Python architecture
- Frontend-backend interaction
- Recommendation system design
- Lightweight personalization

---

## 🤝 Contribution
- Contributions are welcome.
- To contribute:
  - Fork the repository
  - Create a new branch
  - Make your changes
  - Commit them
  - Open a pull request
