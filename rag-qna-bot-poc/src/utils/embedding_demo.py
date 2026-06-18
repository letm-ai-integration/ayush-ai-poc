from sentence_transformers import (
    SentenceTransformer
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def get_embedding_info(text):

    embedding = model.encode(text)

    return {
        "dimensions": len(embedding),
        "sample": embedding[:20].tolist()
    }