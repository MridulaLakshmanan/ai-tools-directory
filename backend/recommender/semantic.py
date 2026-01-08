from embeddings.embedder import embed
from sklearn.metrics.pairwise import cosine_similarity

def semantic_score(query, tool):
    q_emb = embed(query)
    t_emb = embed(
        f"{tool.get('name','')} {tool.get('description','')} {tool.get('category','')}"
    )
    return float(cosine_similarity([q_emb], [t_emb])[0][0])
