from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
def create_faiss_index(texts: list[str]):
  embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
  return FAISS.from_texts(texts,embeddings)

def retrieve_relevant_docs(vectorestore,query:str, k: int=3):
  docs=vectorestore.similarity_search(query, k=k)
  return docs
