# ================================
# Builder Stage (Minimal Install)
# ================================

FROM ubuntu:latest AS builder

WORKDIR /app

# Install essential dependencies
# portaudio19-dev is required for pyaudio
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    portaudio19-dev \ 
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install --upgrade pip && pip3 install uv
RUN uv venv /app/.venv

ARG HUGGINGFACE_TOKEN

# Install embedding model from hugging face <english>
RUN huggingface-cli download BAAI/bge-large-en-v1.5 --local-dir ./Agent/cached_embedding_model --token HUGGINGFACE_TOKEN
#it will automaticly install in correct directory in agents sub folder of Agenetic app 

# Set PATH for virtual environment
ENV PATH="/app/.venv/bin:$PATH"


COPY Agent/API.py /app/Agent/API.py
COPY Agent/Rag.py /app/Agent/Rag.py
COPY Agent/prompt.py /app/Agent/prompt.py
COPY Agent/code_runner_agent.py /app/Agent/code_runner_agent.py
COPY Agent/Data_analyst_API.py /app/Agent/Data_analyst_API.py
COPY Agent/req.txt /app/Agent/req.txt
COPY Agent/storage /app/Agent/storage
COPY Agent/WorldPopulation2023.csv /app/Agent/WorldPopulation2023.csv


# Install dependenciesRun docker build --build-arg HUGGINGFACE_TOKEN=*** -t abdelrahmanmostafamohamed/dataverse_agents:latest .
  
#0 building with "default" instance using docker driver
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 1.95kB done
#1 DONE 0.0s
#2 [internal] load metadata for docker.io/nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
#2 ...
#3 [auth] nvidia/cuda:pull token for registry-1.docker.io
#3 DONE 0.0s
#4 [internal] load metadata for docker.io/nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04



# ================================
# Final Image (Slim Runtime)
# ================================

FROM ubuntu:latest

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder /app/Agent /app/Agent
EXPOSE 8000
CMD ["fastapi","dev","Agent/API.py","--reload","--host","0.0.0.0","--port","8000"]
