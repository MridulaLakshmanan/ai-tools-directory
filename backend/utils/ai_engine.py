# ai_engine.py (robust intent+category detection + semantic recommendation)
import re
from typing import List, Dict, Any, Optional

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    EMBEDDINGS_AVAILABLE = True
except Exception as e:
    # If embeddings packages missing, we'll fall back to keyword scoring
    print("Embedding libraries not available, falling back to keyword scorer.", e)
    EMBEDDINGS_AVAILABLE = False

# === Original lightweight keyword scorer (fallback and baseline) ===
WORD_RE = re.compile(r"[A-Za-z0-9#\+\-]{2,}")

def tokenize(text: str):
    if not text:
        return []
    return [t.lower() for t in WORD_RE.findall(text)]

def score_tool_keyword(query: str, tool: Dict[str, Any]):
    q_tokens = set(tokenize(query))
    if not q_tokens:
        return 0.0
    name_tokens = set(tokenize(tool.get('name', '')))
    desc_tokens = set(tokenize(tool.get('description', '')))
    cat_tokens = set(tokenize(tool.get('category', '')))
    tags = tool.get('tags') or []
    if isinstance(tags, str):
        tags = [s.strip() for s in tags.split(',') if s.strip()]
    tag_tokens = set(tokenize(' '.join(tags)))
    score = 0.0
    score += 3.0 * len(q_tokens & name_tokens)
    score += 2.0 * len(q_tokens & tag_tokens)
    score += 1.0 * len(q_tokens & (desc_tokens | cat_tokens))
    return float(score)

# === Embedding-based recommender (preferred if available) ===
if EMBEDDINGS_AVAILABLE:
    # model: change if you want larger/smarter models
    MODEL_NAME = 'paraphrase-MiniLM-L3-v2'
    model = SentenceTransformer(MODEL_NAME)

    def embed_text(text: str):
        if not text or not text.strip():
            return np.zeros((model.get_sentence_embedding_dimension(),), dtype=float)
        return model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

    # Predefined categories + keywords (keep this list in sync with your frontend categories)
    CATEGORY_KEYWORDS = {
        "AI Assistant": ["assistant", "chatbot", "chat", "agent", "copilot"],
        "Image Generation": ["image", "art", "picture", "visual", "generate", "graphics", "photo"],
        "Video Generation": ["video", "film", "animation", "motion", "edit", "create video", "video generation"],
        "Content Writing": ["write", "content", "blog", "copy", "text", "marketing", "article"],
        "Voice Generation": ["voice", "speech", "audio", "sound", "narration", "talk", "voiceover"],
        "Translation": ["translate", "language", "conversion", "multilingual", "localize"],
        "Development": ["code", "developer", "programming", "build", "software", "IDE"],
        "Productivity": ["workflow", "task", "organize", "project", "notes", "productivity"],
        "Research": ["research", "find info", "analyze", "search", "data", "research tool"],
        "Design": ["design", "template", "layout", "poster", "graphic", "UI", "ux"],
        "Writing Assistant": ["grammar", "proofread", "spelling", "style", "sentence", "editing"]
    }

    # Precompute category embeddings for semantic intent detection
    CATEGORY_EMBEDDINGS = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        combined = cat + " " + " ".join(kws)
        CATEGORY_EMBEDDINGS[cat] = embed_text(combined)

    # Clean a query by removing common filler phrases
    def preprocess_query(query: str) -> str:
        if not query:
            return ""
        q = query.lower().strip()
        q = re.sub(r"\b(i need|show me|find|give me|i want|tools for|apps for|software for|can you|that help with|recommend|looking for)\b", "", q)
        q = re.sub(r"[^a-z0-9\s]", " ", q)
        q = re.sub(r"\s+", " ", q).strip()
        return q

    # Detect category by keyword match first, then embedding similarity as fallback
    def detect_category_intent(query: str, threshold: float = 0.55) -> Optional[str]:
        if not query:
            return None
        q_lower = query.lower()
        # 1) keyword quick match
        for cat, kws in CATEGORY_KEYWORDS.items():
            for w in kws:
                if re.search(rf"\b{re.escape(w)}\b", q_lower):
                    # immediate return on any explicit keyword
                    return cat

        # 2) semantic similarity with category embeddings
        q_emb = embed_text(preprocess_query(query))
        best_cat = None
        best_sim = -1.0
        for cat, c_emb in CATEGORY_EMBEDDINGS.items():
            sim = float(cosine_similarity([q_emb], [c_emb])[0][0])
            if sim > best_sim:
                best_sim = sim
                best_cat = cat
        # Apply threshold so we only pick a category if it's reasonably similar
        if best_sim >= threshold:
            return best_cat
        return None

    def prepare_tool_embeddings(tools: List[Dict[str, Any]]):
        # cache embeddings on tool dict to avoid recomputing every request
        for tool in tools:
            if 'embedding' not in tool or tool['embedding'] is None:
                combined_text = f"{tool.get('name','')} {tool.get('description','')} {tool.get('category','')} {tool.get('tags','')}"
                try:
                    tool['embedding'] = embed_text(combined_text)
                except Exception as e:
                    # fallback: set None and leave for keyword scorer
                    print("Embedding failed for tool:", tool.get('name'), e)
                    tool['embedding'] = None
        return tools

    def recommend(query: str, tools: List[Dict[str, Any]], limit: int = 5):
        """
        Hybrid semantic recommender:
          - detect category intent using keywords or category embeddings
          - compute semantic similarity between query and tool embeddings
          - boost tools whose category matches detected intent or category similarity
          - fallback to keyword scorer if embeddings not available for a tool
        """
        if not query or not query.strip():
            return []

        # Preprocess + detect category intent
        cleaned = preprocess_query(query)
        detected_category = detect_category_intent(query)
        # Prepare embeddings for tools (cached)
        prepare_tool_embeddings(tools)

        # Create query embeddings: one cleaned (for semantic) and raw (for stronger overlap)
        try:
            q_emb = embed_text(cleaned)
            q_raw_emb = embed_text(query)
        except Exception as e:
            print("Query embedding failed, falling back to keyword scorer:", e)
            # Fallback: use keyword scoring across tools
            scored = [(score_tool_keyword(query, t), t) for t in tools]
            scored = [s for s in scored if s[0] > 0]
            scored.sort(key=lambda x: (-x[0], x[1].get('name','')))
            return [t for _, t in scored[:limit]]

        results = []
        # Precompute category embedding similarity (query->category)
        category_sim = {}
        for cat, c_emb in CATEGORY_EMBEDDINGS.items():
            category_sim[cat] = float(cosine_similarity([q_emb], [c_emb])[0][0])

        for tool in tools:
            # If tool has embedding, use semantic similarity
            if tool.get('embedding') is not None:
                sem_sim = float(cosine_similarity([q_emb], [tool['embedding']])[0][0])
                raw_sim = float(cosine_similarity([q_raw_emb], [tool['embedding']])[0][0])
                # hybrid score - you can tweak weights
                base_score = (0.65 * sem_sim) + (0.25 * raw_sim)
            else:
                # fallback to keyword scoring scaled into 0..1 (simple normalization)
                kscore = score_tool_keyword(query, tool)
                # normalize roughly by cap (you can tune)
                base_score = min(kscore / 12.0, 1.0)

            # Category boost if direct match
            bonus = 0.0
            tool_cat = (tool.get('category') or "").lower()

            if detected_category and detected_category.lower() in tool_cat:
                bonus += 0.18  # direct category match bonus

            # Also boost by semantic closeness to the detectedCategory (or best category)
            # If detected_category is None, we still use category_sim to boost tools in categories that are semantically close to the query
            # compute tool's category similarity from precomputed category_sim
            # find tool's category in category_sim keys (case-insensitive)
            best_tool_cat_sim = 0.0
            for c_name, c_sim in category_sim.items():
                if c_name.lower() in tool_cat:
                    best_tool_cat_sim = max(best_tool_cat_sim, c_sim)
            # If we didn't find direct, compute similarity of tool.category text vs query embedding
            if best_tool_cat_sim == 0.0 and tool.get('category'):
                try:
                    cat_emb = embed_text(tool.get('category'))
                    best_tool_cat_sim = float(cosine_similarity([q_emb], [cat_emb])[0][0])
                except Exception:
                    best_tool_cat_sim = 0.0

            # Add a scaled category-sim bonus (small)
            bonus += max(0.0, (best_tool_cat_sim - 0.45)) * 0.25  # only positive when similarity > 0.45

            final_score = float(base_score + bonus)

            results.append((final_score, tool))

        # sort by final_score desc
        results.sort(key=lambda x: x[0], reverse=True)
        # Debug: print top candidates (optional)
        # print("Top candidates:", [(round(s,3), t.get('name')) for s,t in results[:6]])
        return [t for _, t in results[:limit]]

else:
    # If embeddings not available, preserve original functions
    def detect_category_intent(query: str) -> Optional[str]:
        if not query:
            return None
        q_lower = query.lower()
        # simple keyword lookup from CATEGORY_KEYWORDS fallback set:
        FALLBACK_CATEGORY_KEYWORDS = {
            "AI Assistant": ["assistant", "chatbot", "chat", "agent", "copilot"],
            "Image Generation": ["image", "art", "visual", "photo", "picture", "generate"],
            "Video Generation": ["video", "film", "animation", "edit", "motion"],
            "Content Writing": ["write", "content", "blog", "copy", "article"],
            "Voice Generation": ["voice", "speech", "audio", "narration", "voiceover"],
            "Translation": ["translate", "language", "multilingual"],
            "Development": ["code", "developer", "programming"],
            "Productivity": ["workflow", "task", "organize"],
            "Research": ["research", "search", "data"],
            "Design": ["design", "template", "graphic"],
            "Writing Assistant": ["grammar", "proofread", "editing"]
        }
        for cat, kws in FALLBACK_CATEGORY_KEYWORDS.items():
            for w in kws:
                if re.search(rf"\b{re.escape(w)}\b", q_lower):
                    return cat
        return None

    def prepare_tool_embeddings(tools: List[Dict[str, Any]]):
        # no-op in fallback
        return tools

    def recommend(query: str, tools: List[Dict[str, Any]], limit: int = 5):
        # fallback to simple keyword scoring and category boost
        if not query or not query.strip():
            return []
        detected = detect_category_intent(query)
        scored = []
        for t in tools:
            s = score_tool_keyword(query, t)
            if detected and detected.lower() in (t.get('category') or "").lower():
                s += 2.0
            if s > 0:
                scored.append((s, t))
        scored.sort(key=lambda x: (-x[0], x[1].get('name','')))
        return [t for _, t in scored[:limit]]
