from sentence_transformers import SentenceTransformer

# load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):

    if not text:
        return None

    vector = model.encode(text)

    # ensure vector length = 384
    return vector.tolist()