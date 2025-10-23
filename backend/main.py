import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routes.recommend import router as recommend_router

ALLOWED = os.getenv('ALLOWED_ORIGINS','http://localhost:3000').split(',')

app = FastAPI(title='AI Recommender')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED if o.strip()],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/health')
def health():
    return {'status':'ok'}

app.include_router(recommend_router)
