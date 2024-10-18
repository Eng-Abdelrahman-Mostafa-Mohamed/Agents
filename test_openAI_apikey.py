from llama_index.llms.groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv('GROQ_API_KEY'))
llm = Groq(model="llama3-70b-8192", api_key=os.getenv('GROQ_API_KEY'))