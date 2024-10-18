# Import necessary modules after loading the API key
from llama_index.core.tools import FunctionTool
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import torch
import os
import nest_asyncio
from dotenv import load_dotenv
torch.cuda.set_device(0)

load_dotenv()


api_key = os.getenv('GROQ_API_KEY')

if api_key is None:
    print("Error: GROQ_API_KEY is not set. Please set it in your environment or .env file.")
    exit(1)




torch.cuda.set_device(0)

# Initialize the Groq LLM with error handling
try:
    llm = Groq(model="llama3-70b-8192", api_key=api_key)
except Exception as e:
    print(f"Error initializing Groq LLM: {e}")
    exit(1)

# Initialize the embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5",device="cuda" if torch.cuda.is_available() else "cpu")

# Configure global settings to use Groq LLM and HuggingFace embedding
Settings.llm = llm
Settings.embed_model = embed_model
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.num_output = 512
Settings.context_window = 3900

# Load data from the input files
try:
    canada_docs = SimpleDirectoryReader(input_files=["discover.pdf"]).load_data()
except Exception as e:
    print(f"Error loading documents: {e}")
    exit(1)

# Create and store the index using the updated settings
storage_context = StorageContext.from_defaults()
index = VectorStoreIndex.from_documents(
    canada_docs, storage_context=storage_context, show_progress=True, embeded_model=embed_model
)

# Load the index from storage (optional, for subsequent runs)
index = load_index_from_storage(storage_context, persist_dir="./storage")

# Create a query engine using the updated settings
query_engine = index.as_query_engine(llm=llm, verbose=True, max_iter=5)

try:
    response = query_engine.query("give me the basic 10 sentense information about canada 10000 token ?")
    print(response)
except Exception as e:
    print(f"Error during query: {e}")
