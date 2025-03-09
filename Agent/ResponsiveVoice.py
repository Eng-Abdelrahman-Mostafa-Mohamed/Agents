# # import os

# # from fastrtc import (ReplyOnPause, Stream, get_stt_model, get_tts_model)
# # from API import agent
# # stt_model = get_stt_model()
# # tts_model = get_tts_model()


# # def echo(audio):
# #     prompt = str(stt_model.stt(audio).translate("ar"))
# #     response = agent.query(prompt)
# #     for audio_chunk in tts_model.stream_tts_sync(response):
# #         yield audio_chunk

# # stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
# # stream.ui.launch()

# import os
# from fastrtc import ReplyOnPause, Stream, get_stt_model, get_tts_model
# from API import get_agent  # Ensure this is your custom LlamaIndex agent
# import re
# # Load STT and TTS models
# stt_model = get_stt_model()
# tts_model = get_tts_model()

# def echo(audio):
#     """
#     Process audio input, transcribe it, query the agent, and stream the response as audio.
#     """
#     agent=get_agent()
#     try:
#         # Transcribe audio to text
#         prompt = stt_model.stt(audio)  
#         print(f"Transcribed prompt: {prompt}")

#         # Query the agent
#         response = agent.query(prompt)
#         response_text = str(response) 
#         response_text = re.sub(r"\n", " ", response_text) 
#         print(f"Agent response: {response_text}")

#         # Stream the response as audio
#         for audio_chunk in tts_model.stream_tts_sync(response_text):  
#             yield audio_chunk
#     except Exception as e:
#         print(f"Error in echo function: {e}")
#         yield b""  

# # Create and launch the stream
# stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
# stream.ui.launch()



# ## its all from deepseek i havent read  full documentation yet 
# ## the idea that we want to enable LLM Calling to remind me that the running finished or there is problem on data that i collect 

# ## Searching bart that we could apply it as paper how to apply reasoning AI and make llm training based on sft and <Human feedback policy>
# ## revision on sarsa and Deep Q N  to make our owned ploicy human feedbake trainer live with rag
# ## we could make it as a paper and we could apply it on our own data

import os
import re
from fastrtc import ReplyOnPause, Stream, get_stt_model, get_tts_model
from API import get_agent  # Ensure this is your custom LlamaIndex agent

# Load STT and TTS models
stt_model = get_stt_model()
tts_model = get_tts_model()

def clean_text(text):
    """
    Clean the text by removing special characters, extra spaces, and normalizing it.
    """
    # Remove special characters and normalize spaces
    text = re.sub(r"[^\w\s]", "", text)  # Remove non-alphanumeric characters
    text = re.sub(r"\s+", " ", text)  # Normalize multiple spaces to a single space
    text = text.strip()  # Remove leading/trailing spaces
    return text

def echo(audio):
    """
    Process audio input, transcribe it, query the agent, and stream the response as audio.
    """
    agent = get_agent()
    try:
        # Transcribe audio to text
        prompt = stt_model.stt(audio)
        print(f"Transcribed prompt: {prompt}")

        # Clean the transcribed text
        prompt = clean_text(prompt)
        print(f"Cleaned prompt: {prompt}")

        # Query the agent
        response = agent.query(prompt)
        response_text = str(response)
        response_text = clean_text(response_text)  # Clean the agent's response
        print(f"Agent response: {response_text}")

        # Stream the response as audio
        for audio_chunk in tts_model.stream_tts_sync(response_text):
            yield audio_chunk
    except Exception as e:
        print(f"Error in echo function: {e}")
        yield b""  # Yield empty bytes in case of error

# Create and launch the stream
stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
stream.ui.launch()