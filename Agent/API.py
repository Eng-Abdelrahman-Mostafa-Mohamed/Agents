
from fastapi import FastAPI
from Rag import setup_agent 
import uvicorn 
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "welcom"}

agent=None
def get_agent():
    global agent
    if agent is None:
        agent = setup_agent()
    return agent
@app.post("/query/")
async def query(prompt: str):
    agent=get_agent()
    if not agent:
        return {"error": "Failed to initialize agent"}
    
    try:
        result = agent.query(prompt)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}


# Only run Uvicorn when executing this script directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8060)
#     uvicorn.run(app, host="0.0.0.0", port=8000)