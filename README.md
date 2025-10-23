Fullstack package:
- frontend/: static site (index.html, app.js, style.css)
- backend/: FastAPI app (connects to your Supabase)

Instructions (mac):
1. Frontend: open frontend/index.html in browser (live server recommended).
2. Backend:
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with SUPABASE_URL and SUPABASE_KEY
   uvicorn main:app --reload --port 8000
3. In the frontend search box, typing >=2 chars will call the backend for recommendations.
