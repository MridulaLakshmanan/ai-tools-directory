import re

WORD_RE = re.compile(r"[a-zA-Z0-9]+")

def tokenize(text):
    return set(t.lower() for t in WORD_RE.findall(text))

def keyword_score(query, tool):
    q = tokenize(query)
    t = tokenize(
        f"{tool.get('name','')} {tool.get('description','')} {tool.get('category','')}"
    )
    if not q:
        return 0.0
    return len(q & t) / len(q)
