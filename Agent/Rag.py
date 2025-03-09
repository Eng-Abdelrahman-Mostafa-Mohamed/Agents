import os
import pandas as pd
from llama_index.core import ServiceContext, set_global_service_context
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq
from prompt import new_prompt, instruction_str
from Notes import note_engine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import ReActAgent
from langchain_huggingface import HuggingFaceEmbeddings
from code_runner_agent import code_runner_engine
from llama_index.core.memory import ChatMemoryBuffer
from dotenv import load_dotenv
import torch
from fastapi import FastAPI
import uvicorn

torch.cuda.set_device(0)
load_dotenv()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
app = FastAPI()

def setup_agent():

    llm = Groq(model="llama3-70b-8192", api_key=os.getenv('GROQ-API-KEY'))
    model_name = "BAAI/bge-small-en-v1.5"
    model_dir = "./Agent/cached_embedding_model/snapshots/d4aa6901d3a41ba39fb536a557fa166f842b0e09"
    if os.path.exists(model_dir):
        print("Cached model found locally...")
    
        embed_model = HuggingFaceEmbeddings(model_name=model_name, cache_folder=model_dir)
    else:
        print("Downloading model...")
        embed_model = HuggingFaceEmbeddings(model_name=model_name)
        print("Saving model locally...")
        embed_model.save_pretrained(model_dir)
        
    
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
    Settings.num_output = 512
    Settings.context_window = 3900

    data_name = "Agent/WorldPopulation2023.csv"
    try:
        data = pd.read_csv(data_name)
        print("✅ Data loaded successfully")
    except FileNotFoundError:
        print("❌ File not found. Please check the file path.")
        return None
    print(data.head())
    
    
    population_pandas_query_engine = PandasQueryEngine(
        df=data,
        llm=llm,
        verbose=True,
        instruction_str=instruction_str,
        synthesize_response=True,
    )

    population_pandas_query_engine.update_prompts({"pandas_prompt": new_prompt})

    tools = [
        QueryEngineTool.from_defaults(
            query_engine=population_pandas_query_engine,
            name="population_data",
            description="Provides world population statistics.",
        ),
        note_engine,
        code_runner_engine,
    ]

    memory = ChatMemoryBuffer(token_limit=100)

    agent = ReActAgent(
        tools=tools,
        llm=llm,
        verbose=True,
        context=f'The agent assists users with world population data from {data_name}, generating and executing code.',
        memory=memory,
        max_iterations=10000,
        
    )

    return agent

#### i moved it to separated folder to be able to run it in a separated process

# responser_noter_codeGeneration_agent = setup_agent()

# while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    
#     try:
#         result = responser_noter_codeGeneration_agent.query(prompt)
#         # Print the agent's response
#         print("Agent Response:")
#         print(result)
#     except Exception as e:
#         print(f"An error occurred: {e}")
# agent=None
# def get_agent():
#     global agent
#     if agent is None:
#         agent = setup_agent()
#     return agent


# @app.get("/")
# async def root():
#     return {"message": "welcom"}


# @app.post("/query/")
# async def query(prompt: str):
#     agent=get_agent()
#     if not agent:
#         return {"error": "Failed to initialize agent"}
    
#     try:
#         result = agent.query(prompt)
#         return {"response": result}
#     except Exception as e:
#         return {"error": str(e)}


# # Only run Uvicorn when executing this script directly
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8020)

