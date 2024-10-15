from llama_index.core.tools import FunctionTool
from llama_index.core.readers import SimpleDirectoryReader 
from llama_index.core  import VectorStoreIndex ,StorageContext ,load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.groq import Groq
import os
import nest_asyncio
nest_asyncio.apply()

os.environ['OPENAI_API_KEY'] = 'sk-mFBq7t6V5-OGh223N1le4a4q8RCoLjUUFU4Fms-7B5T3BlbkFJTOnS6lFV5F03K66Okiy1uKKOgBVLFSw7BLlKh4gtsA'
os.environ['OPENAI_API_KEY'] = 'sk-mFBq7t6V5-OGh223N1le4a4q8RCoLjUUFU4Fms-7B5T3BlbkFJTOnS6lFV5F03K66Okiy1uKKOgBVLFSw7BLlKh4gtsA'
llm = Groq(model="llama3-70b-8192", api_key=os.getenv('GROQ-API-KEY'))
Settings.llm = llm
Settings.node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
Settings.embed_model = llm
Settings.num_output = 512
Settings.context_window = 3900

canada_docs = SimpleDirectoryReader(input_files=["discover.pdf"]).load_data()
Splitter=SentenceSplitter(chunk_size=1024)
nodes = Splitter.get_nodes_from_documents(canada_docs)
vector_index = VectorStoreIndex(nodes)
query_engin_pdf = vector_index.as_query_engine(llm=llm,verbose=True,)

print(query_engin_pdf.query("what is the capital of canada?"))