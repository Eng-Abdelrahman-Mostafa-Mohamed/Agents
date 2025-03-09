
# ================================
# Builder image stage
# ================================
FROM ubuntu:22.04 AS builder

WORKDIR /app

# Install essential dependencies
# portaudio19-dev is required for pyaudio
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    portaudio19-dev \ 
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && pip3 install uv
RUN uv venv /app/.venv

ARG HUGGINGFACE_TOKEN

# Install embedding model from hugging face <english>
RUN huggingface-cli download BAAI/bge-large-en-v1.5 --local-dir ./Agent/cached_embedding_model --token $HUGGINGFACE_TOKEN

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

RUN uv pip install -r Agent/req.txt



# ================================
# Final Image (Slim Runtime)
# ================================

FROM ubuntu:22.04 AS final

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder /app/Agent /app/Agent
EXPOSE 8000
CMD ["fastapi","dev","Agent/API.py","--reload","--host","0.0.0.0","--port","8000"]
