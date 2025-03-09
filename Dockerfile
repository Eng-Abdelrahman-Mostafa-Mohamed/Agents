# ================================
# Builder Stage (Minimal Install)
# ================================
FROM nvidia/cuda:12.4.1-cudnn8-devel-ubuntu22.04 AS builder

WORKDIR /app

# Install essential dependencies
# portaudio19-dev is required for pyaudio
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    portaudio19-dev \ 
    && rm -rf /var/lib/apt/lists/*

# Install uv and create virtual environment
RUN pip3 install --upgrade pip && pip3 install uv
RUN uv venv /app/.venv

# Install embedding model from hugging face <english>
RUN huggingface-cli download BAAI/bge-large-en-v1.5 --local-dir ./Agent/cached_embedding_model
#it will automaticly install in correct directory in agents sub folder of Agenetic app 

# Set PATH for virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy only required files
COPY req.txt /app/
COPY Agent/API.py /app/Agent/API.py
COPY Agent/Rag.py /app/Agent/Rag.py
COPY Agent/prompt.py /app/Agent/prompt.py
COPY Agent/code_runner_agent.py /app/Agent/code_runner_agent.py
COPY Agent/Data_analyst_API.py /app/Agent/Data_analyst_API.py
COPY Agent/req.txt /app/Agent/req.txt
COPY Agent/storage /app/Agent/storage
COPY Agent/cached_embedding_model /app/Agent/cached_embedding_model
COPY Agent/bge-large-en-v1.5 /app/Agent/bge-large-en-v1.5
COPY Agent/WorldPopulation2023.csv /app/Agent/WorldPopulation2023.csv


# Install dependencies
RUN uv pip install -r req.txt
RUN uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124



# ================================
# Final Image (Slim Runtime)
# ================================

FROM nvidia/cuda:12.4.1-cudnn8-runtime-ubuntu22.04

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder /app/Agent /app/Agent
EXPOSE 8000
RUN cd Agent
CMD ["python", "-m", "uvicorn", "API:app", "--host", "0.0.0.0", "--port", "9000", "--workers", "4"]
