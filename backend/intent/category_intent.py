import re

CATEGORY_KEYWORDS = {
    "Content Writing": ["write", "blog", "content", "copy", "article"],
    "Writing Assistant": ["grammar", "proofread", "rewrite"],
    "Image Generation": ["image", "art", "photo", "visual"],
    "Video Generation": ["video", "edit", "animation"],
    "Development": ["code", "developer", "programming"],
    "Productivity": ["task", "workflow", "organize"],
}

def detect_category_intent(query: str):
    q = query.lower()
    for category, words in CATEGORY_KEYWORDS.items():
        for w in words:
            if re.search(rf"\b{w}\b", q):
                return category
    return None
