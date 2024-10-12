from llama_index.core.tools import FunctionTool
from llama_index.core.readers import SimpleDirectoryReader 
from llama_index.core  import VectorStoreIndex ,StorageContext ,load_index_from_storage

canada_docs = SimpleDirectoryReader(
    path="/home/abdelrahman/Documents/learning_RAG/Canada",
    file_pattern="*.pdf",
    encoding="utf-8",
    language="en",
    max_docs=None,
    name="canada_docs",
    description="A collection of PDF documents about Canada.",
)