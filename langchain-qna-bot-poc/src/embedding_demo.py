from sentence_transformers import SentenceTransformer
model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
def get_embedding_info(text):
 emb=model.encode(text)
 return {'dimensions':len(emb),'sample':emb[:20].tolist()}
