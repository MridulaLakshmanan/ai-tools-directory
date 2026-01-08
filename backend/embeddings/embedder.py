from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

def embed(text: str):
    return _model.encode(text, normalize_embeddings=True)
