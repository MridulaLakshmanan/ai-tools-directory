# 🤖 All I Need AI — AI Tools Directory

> Discover, search, and get personalized recommendations for 700+ AI tools across 14 categories — powered by semantic search, RAG-based AI advisor, and a fully automated scraping pipeline.

---

## 🌐 Live Project

**Frontend:** Vanilla HTML/CSS/JS · Served via Live Server  
**Backend:** FastAPI (Python) · Port 8001  
**Database:** Supabase (PostgreSQL + pgvector)  
**AI Advisor:** Groq Llama 3.3 70B via Supabase Edge Functions  

---

## 📌 Project Overview

All I Need AI is a full-stack AI tools directory that helps users discover the right AI tool for their specific use case. It combines traditional keyword search, semantic vector search, and a RAG-powered AI chatbot to provide accurate, context-aware tool recommendations from a curated database of 693 tools.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Semantic Search** | Weighted full-text search using PostgreSQL `tsvector` with name/description/category ranking |
| 🤖 **RAG AI Chatbot** | Retrieval-Augmented Generation — fetches real tools from DB, injects into Llama 3.3 prompt |
| 🕷️ **AI-Powered Scraper** | Playwright + Groq LLM extraction from GitHub repos and AI directories |
| 🧠 **Vector Embeddings** | 384-dim `all-MiniLM-L6-v2` embeddings stored in pgvector for semantic similarity |
| ⚡ **Edge Function Proxy** | Groq API key secured server-side via Supabase Edge Functions (Deno/TypeScript) |
| 📊 **Live Stats** | Dynamic hero stats fetched from Supabase on page load with animated counters |
| 🔖 **Favorites** | Supabase auth-based favorites system per user |
| 📁 **Category Filters** | Live category counts fetched from DB, single-query bulk name cache |
| 🌗 **Glassmorphic UI** | Dark futuristic design with particle canvas, CSS animations, responsive layout |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│   HTML + CSS + Vanilla JS (app.js + chatbot.js)         │
│   Particle canvas · Category filters · Tool grid        │
│   Submission modal · Favorites · View toggle            │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────┐    ┌─────────────────────────────┐
│   FastAPI Backend    │    │    Supabase (PostgreSQL)     │
│   Python 3.9        │    │                             │
│                      │    │  ai_tools table             │
│  /api/recommend      │    │  - pgvector embeddings      │
│   ↓                  │    │  - GIN full-text index      │
│  Tool cache (10min)  │◄───│  - HNSW vector index        │
│  Keyword pre-filter  │    │  - search_tools() RPC       │
│  Batch embeddings    │    │  - match_tools() RPC        │
│  Cosine similarity   │    │                             │
│  Category intent     │    │  favorites table            │
│                      │    │  auth.users                 │
└──────────────────────┘    └──────────┬──────────────────┘
                                       │
                            ┌──────────▼──────────────────┐
                            │   Supabase Edge Functions   │
                            │   (Deno · TypeScript)       │
                            │                             │
                            │  ai-advisor                 │
                            │  → Groq API proxy           │
                            │  → Key never in browser     │
                            │                             │
                            │  generate-embeddings        │
                            │  → HuggingFace API          │
                            │  → Fills missing vectors    │
                            └─────────────────────────────┘
```

---

## 🕷️ AI Scraping Pipeline

```
Sources → Playwright/Jina → Groq LLM Extraction → Normalize → Deduplicate → Supabase
```

**Sources scraped:**
- 8× GitHub awesome-list repositories
- Futurepedia.io (paginated)
- AI tool directories via Jina Reader

**Traditional → AI scraping upgrade:**

| Old approach | New approach |
|---|---|
| BeautifulSoup tag hunting | Groq Llama 3.3 extracts structured JSON |
| Breaks on site redesign | Works on any layout automatically |
| Categories come in as "Other" | LLM assigns correct category from 14 options |
| Single GitHub repo | 8 repos scraped with parallel workers |
| ~346 tools | 693 tools |

**Rate limit strategy:** 25s delay between chunks, exponential backoff (30s→60s→120s), sequential processing to avoid shared rate limit conflicts.

---

## 🧠 RAG Chatbot Architecture

```
User Query
    ↓
1. detectCategory()      — keyword mapping to 14 categories
    ↓
2. fetchToolsFromDB()    — Supabase search_tools() RPC → 15 real tools
    ↓
3. callEdgeFunction()    — injects real tools into Llama 3.3 prompt
                         — "Only pick from THIS list"
    ↓
4. enrichWithDBData()    — maps LLM picks back to real DB records
                         — attaches real id, website, rating, pricing
    ↓
Tool cards with real data → open modal / filter grid / visit site
```

**Security:** Groq API key stored as Supabase Edge Function secret — never in any frontend file, safe to push to GitHub.
<img width="1470" height="831" alt="Screenshot 2026-03-25 at 10 31 15 PM" src="https://github.com/user-attachments/assets/355489fa-fe56-46b0-82e3-c3ffa150cd64" />


---

## 🔍 Search Architecture

**PostgreSQL weighted full-text search:**

```sql
setweight(to_tsvector('english', name), 'A')        -- 3× weight
setweight(to_tsvector('english', description), 'B') -- 1× weight  
setweight(to_tsvector('english', category), 'C')    -- 0.5× weight
```

**Backend semantic search pipeline:**

1. Tools cached in memory (10-min TTL) — no DB call per request
2. Keyword pre-filter → top 100 candidates
3. Query embedded once → batch cosine similarity on 100 tools
4. Category intent detection boosts relevant results by +0.15
5. Relevance threshold (0.45) filters noise

**Latency improvement:** 5–10s → ~200–500ms after caching + batch scoring.

---

## 🗄️ Database Schema

```sql
ai_tools (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name        TEXT NOT NULL,
  description TEXT,
  category    TEXT,           -- 14 curated categories
  tags        TEXT[],
  url         TEXT,
  website     TEXT,
  rating      NUMERIC,
  pricing     TEXT,
  embedding   VECTOR(384),    -- all-MiniLM-L6-v2 embeddings
  approved    BOOLEAN DEFAULT false,
  added_by    TEXT DEFAULT 'community',
  search_vector TSVECTOR      -- pre-computed weighted FTS vector
)

Indexes:
  - idx_ai_tools_embedding_hnsw  (HNSW, vector_cosine_ops)
  - idx_ai_tools_search_vector   (GIN, for full-text search)
  - idx_ai_tools_category        (btree)
  - idx_ai_tools_name            (btree)
  - idx_ai_tools_approved        (btree)
```

---

## 📦 Tech Stack

**Frontend**
- Vanilla HTML5, CSS3, JavaScript (ES6+)
- Supabase JS SDK (auth, favorites, category filters)
- Canvas API (animated particle background)

**Backend**
- Python 3.9, FastAPI, Uvicorn
- sentence-transformers (`all-MiniLM-L6-v2`)
- scikit-learn (cosine similarity)
- supabase-py

**Scraper**
- Playwright (browser automation)
- Groq API — `llama-3.3-70b-versatile` (AI extraction)
- Jina Reader API (free URL→markdown conversion)
- Threading (parallel worker support)

**Database & Infrastructure**
- Supabase (PostgreSQL 15 + pgvector extension)
- Supabase Edge Functions (Deno/TypeScript)
- Supabase Auth (user accounts, favorites)
- Hugging Face Inference API (embedding generation)

---
<img width="1470" height="835" alt="Screenshot 2026-03-25 at 10 30 37 PM" src="https://github.com/user-attachments/assets/7ca6b989-5f87-495f-985c-6c49a04221de" />

<img width="1470" height="836" alt="Screenshot 2026-03-25 at 10 30 54 PM" src="https://github.com/user-attachments/assets/18a4798e-b95d-4b00-8ef5-1ce54abc3216" />


## 📂 Project Structure

```
ai-tools-directory/
├── frontend/
│   ├── index.html          # Main directory page
│   ├── app.js              # Tool grid, search, filters, modals
│   ├── chatbot.js          # RAG AI advisor chatbot
│   └── style.css           # Glassmorphic dark UI
│
└── backend/
    ├── main.py             # FastAPI app + CORS + model warmup
    ├── run_scraper.py      # Master scraper entry point
    ├── run_futurepedia.py  # Standalone Futurepedia scraper
    │
    ├── scraper/
    │   ├── sources/
    │   │   ├── github_scraper.py       # 8 GitHub awesome lists
    │   │   ├── futurepedia_scraper.py  # Paginated scraper
    │   │   └── theresanai_scraper.py   # Directory scraper
    │   └── pipeline/
    │       ├── groq_extractor.py   # AI-powered tool extraction
    │       ├── normalize.py        # Supabase schema shaping
    │       ├── deduplicate.py      # Name-based deduplication
    │       └── embedding.py        # sentence-transformers
    │
    ├── embeddings/
    │   └── embedder.py         # Singleton model (loads once)
    │
    ├── recommender/
    │   ├── ai_engine.py        # Keyword pre-filter + semantic scoring
    │   └── semantic.py         # Batch cosine similarity
    │
    ├── routes/
    │   └── recommend.py        # /api/recommend with 10-min cache
    │
    ├── intent/
    │   └── category_intent.py  # Query → category detection
    │
    ├── models/
    │   └── schemas.py          # Pydantic request/response models
    │
    └── utils/
        ├── supabase_client.py  # DB connection singleton
        └── keyword.py          # Keyword scoring utility
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js (for Live Server)
- Supabase account
- Groq API key (free at console.groq.com)
- Hugging Face account (free at huggingface.co)

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Copy and fill in your keys
cp .env.example .env

# Start the API server
python main.py
```

### Environment Variables (backend/.env)

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_TABLE=ai_tools
GROQ_API_KEY=your_groq_key
GROQ_API_KEY_2=your_second_groq_key  # optional, for parallel scraping
```

### Frontend Setup

Open `frontend/index.html` with Live Server (VS Code extension) or any static server.

### Run the Scraper

```bash
cd backend
python run_scraper.py
```

### Generate Missing Embeddings

```bash
curl -X POST https://your-project.supabase.co/functions/v1/generate-embeddings \
  -H "Authorization: Bearer your_anon_key"
```

---

## 📊 Database Stats

| Metric | Value |
|---|---|
| Total tools | 693 |
| Categories | 14 |
| Tools with embeddings | 683 |
| Largest category | Development & Code (191) |
| Sources scraped | GitHub (8 repos) + directories |

---

## 🔐 Security

- Groq API key stored as Supabase Edge Function secret (never in frontend code)
- Supabase anon key used for read-only DB access (safe to expose)
- `.env` file in `.gitignore` — no secrets in repository
- RLS policies can be enabled per-table for row-level security

---

## 🎯 Motivation

With hundreds of AI tools emerging daily, users struggle to find the right tool for their needs.  
This project is Built to discover new tools and also to explore the high end!!

## 📄 License

MIT License — feel free to fork, extend, and build on top of this project.
