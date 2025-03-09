# # from fastapi import FastAPI
# # from Rag import setup_agent
# # from fastapi.responses import HTMLResponse
# # from  ResponsiveVoice import stt_prompt ,tts_response
# # from fastrtc import Stream, ReplyOnPause
# # import uvicorn
# # import requests
# # import threading
# # import time

# # app = FastAPI()

# # @app.get("/", response_class=HTMLResponse)
# # async def root():
# #     return """
# #     <html>
# #         <head>
# #             <title>Welcome to DataVerse</title>
# #         </head>
# #         <body>
# #             <h1>Welcome to the DataVerse</h1>
# #             <p>Use the /query endpoint to query the agent</p>
# #         </body>
# #     </html>
# #     """

# # @app.post("/query_response/")
# # async def query_response(prompt: str):
# #     agent = setup_agent()
# #     if not agent:
# #         return {"error": "Failed to initialize agent"}
    
# #     try:
# #         result = agent.query(prompt)
# #         return {"response": result}
# #     except Exception as e:
# #         return {"error": str(e)}

# # def run_server():
# #     uvicorn.run(app, host="127.0.0.1", port=5000)

# # if __name__ == "__main__":
# #     # Start the server in a separate thread
# #     converted_to_text_prompt = stt_prompt()

# #     server_thread = threading.Thread(target=run_server)
# #     server_thread.daemon = True  
# #     server_thread.start()

# #     # Wait for the server to start (optional, but recommended)
# #     time.sleep(2)

# #     # Make a POST request to the server
# #     try:
# #         response = requests.post(
# #             "http://127.0.0.1:5000/query_response/",
# #             json={"prompt": converted_to_text_prompt}
# #         )
# #         print(f"The response of the agent is: {response.text}")  
# #         tts_response(response.text)
# #         stream = Stream(ReplyOnPause(stt_prompt), modality="audio", mode="send-receive")
# #         stream.ui.launch()
# #     except Exception as e:
# #         print(f"An error occurred while making the request: {e}")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# #         # from fastapi import FastAPI
# # # from Rag import setup_agent
# # # from fastapi.responses import HTMLResponse
# # # import uvicorn
# # # from ResponsiveVoice import converted_to_text_prompt
# # # import requests
# # # import threading
# # # app = FastAPI()

# # # @app.get("/",response_class=HTMLResponse)
# # # async def root():
# # #     return """
# # #     <html>
# # #         <head>
# # #             <title>Welcome to DataVerse</title>
# # #         </head>
# # #     <body>
# # #         <h1>Welcome to the DataVerse</h1>
# # #         <p>Use the /query endpoint to query the agent</p>
# # #     </body>
# # #     </html>
# # # """

# # # @app.post("/query_response/")
# # # async def query(prompt: str):
# # #     agent = setup_agent()
# # #     if not agent:
# # #         return {"error": "Failed to initialize agent"}
    
# # #     try:
# # #         result = agent.query(prompt)
# # #         return {"response": result}
# # #     except Exception as e:
# # #         return {"error": str(e)}

# # # def run_server():
# # #     uvicorn.run(app, host="127.0.0.1", port=8000)

# # # # Start the server in a separate thread


# # # # Wait for the server to start (optional, but recommended)
# # # import time
# # # time.sleep(2) 

# # # if __name__ == "__main__":
# # #     # uvicorn.run(app, host="127.0.0.1", port=8000)
# # #     server_thread = threading.Thread(target=run_server)
# # #     server_thread.daemon = True  
# # #     server_thread.start()
    
# # #     requests.post("http://127.0.0.1:8000/query_response/", json={"prompt": converted_to_text_prompt})
# # #     response = requests.get("http://127.0.0.1:8000/query_response/")
    
# # #     print(f"the response of agent is : response.text()")


# from fastapi import FastAPI, HTTPException
# from fastapi.responses import HTMLResponse, StreamingResponse
# import uvicorn
# import threading
# import time
# import requests
# import sounddevice as sd
# import numpy as np
# import sys
# import fastrtc as rtc
# from fastrtc import get_tts_model, get_stt_model, Stream, ReplyOnPause
# from ResponsiveVoice import stt_prompt, tts_response_generator
# # Import your agent setup from Rag (adjust if needed)
# from Rag import setup_agent

# app = FastAPI()

# # ------------------------------
# # FastAPI Endpoints
# # ------------------------------
# @app.get("/", response_class=HTMLResponse)
# async def root():
#     html_content = """
#     <html>
#         <head>
#             <title>Welcome to DataVerse</title>
#         </head>
#         <body>
#             <h1>Welcome to the DataVerse</h1>
#             <p>Use the /query_response endpoint to query the agent</p>
#         </body>
#     </html>
#     """
#     return html_content

# @app.post("/query_response/")
# async def query_response(prompt: str):
#     agent = setup_agent()
#     if not agent:
#         raise HTTPException(status_code=500, detail="Failed to initialize agent")
#     try:
#         result = agent.query(prompt)
#         return {"response": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/tts/")
# async def stream_tts(text: str):
#     """
#     Endpoint to stream TTS audio for a given text.
#     """
#     return StreamingResponse(tts_response_generator(text), media_type="audio/wav")


# def run_server():
#     uvicorn.run(app, host="127.0.0.1", port=5000)
    
# if __name__ == "__main__":
#     # Start FastAPI server in a background thread
#     server_thread = threading.Thread(target=run_server)
#     server_thread.daemon = True  
#     server_thread.start()
#     time.sleep(2)  # Wait a moment for the server to start

#     # Use speech-to-text to capture the user prompt
#     try:
#         prompt_text = stt_prompt()
#     except Exception as e:
#         print(f"Error in STT: {e}")
#         prompt_text = "default prompt"

#     # Make a POST request to the /query_response endpoint with the transcribed prompt
#     try:
#         response = requests.post(
#             "http://127.0.0.1:5000/query_response/",
#             json={"prompt": prompt_text}
#         )
#         response_data = response.json()
#         print(f"The response of the agent is: {response_data}")
#     except Exception as e:
#         print(f"An error occurred while making the request: {e}")
#         response_data = {"response": ""}

#     # Convert the agent's response text to audio (streaming TTS)
#     try:
#         print("Streaming TTS audio chunks:")
#         for audio_chunk in tts_response_generator(response_data.get("response", "")):
#             # Here we simply print the length of each audio chunk.
#             # In a real application, you would play or stream the audio.
#             print("Received audio chunk of length:", len(audio_chunk))
#     except Exception as e:
#         print(f"An error occurred during TTS streaming: {e}")

#     # Optionally, launch a real-time streaming UI for continuous conversation
#     try:
#         stream = Stream(ReplyOnPause(stt_prompt), modality="audio", mode="send-receive")
#         stream.ui.launch()
#     except Exception as e:
#         print(f"Error launching real-time streaming UI: {e}")

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
    uvicorn.run(app, host="127.0.0.1", port=8020)
#     uvicorn.run(app, host="0.0.0.0", port=8000)