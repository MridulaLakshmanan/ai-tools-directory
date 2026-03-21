"""
backend/embeddings/embedder.py
--------------------------------
REPLACE your existing embedder.py

The model is loaded at module import time using a background thread
so it's ready before the first request comes in.
"""

import threading
from sentence_transformers import SentenceTransformer

_model = None
_model_ready = threading.Event()

def _load_model():
    global _model
    print("[Embedder] Loading model in background...")
    _model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    _model_ready.set()
    print("[Embedder] ✅ Model ready")

# Start loading immediately when module is imported
threading.Thread(target=_load_model, daemon=True).start()


def embed(text: str):
    """
    Embed text. Waits for model if still loading (only on very first request
    if it arrives before the ~3s load completes).
    """
    if not text or not text.strip():
        return [0.0] * 384

    # Wait max 30s for model — should always be ready well before this
    _model_ready.wait(timeout=30)

    return _model.encode(text.strip(), normalize_embeddings=True)