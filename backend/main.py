"""
backend/main.py
----------------
REPLACE your existing main.py

Imports embedder at startup so model begins loading immediately
when server starts — not when first request arrives.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# ── Trigger model loading at server startup ───────────────────────────────────
import embeddings.embedder  # noqa: F401

from routes.recommend import router as recommend_router

ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app = FastAPI(title="AI Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(recommend_router)