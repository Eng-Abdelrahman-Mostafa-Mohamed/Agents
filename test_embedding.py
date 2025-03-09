import os
from langchain_huggingface import HuggingFaceEmbeddings

model_name = "BAAI/bge-large-en-v1.5"
# cache_dir = "/home/abdelrahman/.cache/huggingface/hub/models--BAAI--bge-large-en-v1.5/snapshots/d4aa6901d3a41ba39fb536a557fa166f842b0e09/"
cache_dir = "Agents/cached_embedding_model/snapshots/d4aa6901d3a41ba39fb536a557fa166f842b0e09"

try:
    embeddings = HuggingFaceEmbeddings(model_name=cache_dir)
    print(f"Embedding model loaded from local cache.")

    sentences = ["This is an example sentence.", "Each sentence is converted"]
    embeddings_result = embeddings.embed_documents(sentences)
    print(embeddings_result)

except Exception as e:
    print(f"Error loading embedding model: {e}")