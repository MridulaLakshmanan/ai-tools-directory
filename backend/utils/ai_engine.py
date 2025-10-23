import re
from typing import List, Dict, Any

WORD_RE = re.compile(r"[A-Za-z0-9#\+\-]{2,}")

def tokenize(text: str):
    if not text: return []
    return [t.lower() for t in WORD_RE.findall(text)]

def score_tool(query: str, tool: Dict[str, Any]):
    q_tokens = set(tokenize(query))
    if not q_tokens: return 0.0
    name_tokens = set(tokenize(tool.get('name','')))
    desc_tokens = set(tokenize(tool.get('description','')))
    cat_tokens = set(tokenize(tool.get('category','')))
    tags = tool.get('tags') or []
    if isinstance(tags, str):
        tags = [s.strip() for s in tags.split(',') if s.strip()]
    tag_tokens = set(tokenize(' '.join(tags)))
    score = 0.0
    score += 3.0 * len(q_tokens & name_tokens)
    score += 2.0 * len(q_tokens & tag_tokens)
    score += 1.0 * len(q_tokens & (desc_tokens | cat_tokens))
    return score

def recommend(query: str, tools: List[Dict[str, Any]], limit: int=5):
    scored = [(score_tool(query, t), t) for t in tools]
    scored = [s for s in scored if s[0] > 0]
    scored.sort(key=lambda x: (-x[0], x[1].get('name','')))
    return [t for _, t in scored[:limit]]
