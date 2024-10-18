import os
import pandas as pd
from ollama import *
from llama_index.core import ServiceContext, set_global_service_context
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq
from adapter.Adapter import Adapter
from sentence_transformers import SentenceTransformer
from prompt import new_prompt, instruction_str
from nomic import embed 
from Notes import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
# from llama_index.core.selectors import LLMMultiSelector, PydanticMultiSelector
# from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from code_runner_agent import code_runner_engine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
from pdf import embed_model
import torch 
torch.set_default_device('cuda')
load_dotenv()

# Set your API keys
# os.environ['GROQ-API-KEY'] = 'Your GROQ API Key'

# os.environ['OPENAI_API_KEY'] = 'Your OpenAI API Key' <<<replaced with local embedding model which is  ("BAAI/bge-small-en-v1.5"") >>>

# Initialize the Groq model with the Llama version 3 
print(os.getenv('GROQ-API-KEY'))
llm = Groq(model="llama3-70b-8192", api_key=os.getenv('GROQ-API-KEY'))

# Set the LLM and embedding model in the settings
Settings.llm = llm
# Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002", embed_batch_size=100,api_key=os.getenv('OPENAI_API_KEY'))
Settings.embed_model = embed_model
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.num_output = 512
Settings.context_window = 3900

# Load the population data
try:
    data_name ="WorldPopulation2023.csv"
    data = pd.read_csv('WorldPopulation2023.csv')
    print("Data loaded successfully")
except FileNotFoundError:
    print("File not found. Please check the file path.")
    exit()

data_str = str(data.head())
print(data)

# Initialize the Pandas Query Engine
population_pandas_query_engine = PandasQueryEngine(
    df=data,
    data_str=data_str,
    llm=llm,
    verbose=True,
    instruction_str=instruction_str,
    synthesize_response=True,
    max_iterations=10000,
)

population_pandas_query_engine.update_prompts({"pandas_prompt": new_prompt})

# Create tools for the agent
tools = [
    QueryEngineTool.from_defaults(
        query_engine=population_pandas_query_engine,
        name="population_data",
        description="Provides information on world population and demographics.",
    ),
    note_engine,
    code_runner_engine,
]

# Initialize the memory buffer
memory = ChatMemoryBuffer(token_limit=100)

# Initialize the agent with memory
responser_noter_codeGeneration_agent = ReActAgent(
    tools=tools,
    llm=llm,
    verbose=True,
    context=f'The agent assists users by providing accurate information about world population statistics of local data which is {data_name}, generating code, and executing it.',
    memory=memory,
    max_iterations=10000,
)

# Main loop for user interaction
while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    
    try:
        result = responser_noter_codeGeneration_agent.query(prompt)
        # Print the agent's response
        print("Agent Response:")
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")
