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
RUN huggingface-cli download BAAI/bge-large-en-v1.5 --local-dir ./Agents/cached_embedding_model
#it will automaticly install in correct directory in agents sub folder of Agenetic app 

# Set PATH for virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy only required files
COPY req.txt /app/
COPY Agents/API.py /app/Agents/API.py
COPY Agents/Rag.py /app/Agents/Rag.py
COPY Agents/prompt.py /app/Agents/prompt.py
COPY Agents/code_runner_agent.py /app/Agents/code_runner_agent.py
COPY Agents/Data_analyst_API.py /app/Agents/Data_analyst_API.py
COPY Agents/req.txt /app/Agents/req.txt
COPY Agents/storage /app/Agents/storage
COPY Agents/cached_embedding_model /app/Agents/cached_embedding_model
COPY Agents/bge-large-en-v1.5 /app/Agents/bge-large-en-v1.5
COPY Agents/WorldPopulation2023.csv /app/Agents/WorldPopulation2023.csv


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
COPY --from=builder /app/Agents /app/Agents
EXPOSE 8000
CMD ["uv","python","./Agents/API.py"]
