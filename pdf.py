
# !pip install llama-index # Install the necessary package
# !pip install llama-index-llms-groq # Install the necessary package
# !pip install llama-index-core # Install the necessary package

from llama_index.core.tools import FunctionTool
from llama_index.core.readers import SimpleDirectoryReader 
from llama_index.core  import VectorStoreIndex ,StorageContext ,load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.langchain import LangchainEmbedding # Import from the correct location
from langchain.embeddings import HuggingFaceEmbeddings
import os
import nest_asyncio
from dotenv import load_dotenv
import torch
torch.cuda.set_device(0)
load_dotenv()
nest_asyncio.apply()

# os.environ['GROQ-API-KEY'] = 'Your GROQ API Key'
# os.environ['OPENAI_API_KEY'] = 'Your OpenAI API Key'

llm = Groq(model="llama3-70b-8192", api_key=os.getenv('GROQ-API-KEY'))
embed_model = LangchainEmbedding(
    HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
)

Settings.llm = llm
Settings.embed_model = embed_model
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.num_output = 512
Settings.context_window = 3900

canada_docs = SimpleDirectoryReader(input_files=["discover.pdf"]).load_data()
Splitter=SentenceSplitter(chunk_size=1024)
nodes = Splitter.get_nodes_from_documents(canada_docs)
vector_index = VectorStoreIndex(nodes)
query_engin_pdf = vector_index.as_query_engine(llm=llm,verbose=True,max_iter=10)

print(query_engin_pdf.query("what is the basic way for life in canada?"))