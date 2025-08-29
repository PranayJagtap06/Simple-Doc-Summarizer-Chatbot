FROM python:3.13-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    neovim axel \
    tesseract-ocr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /backend

# Copy requirements and install dependencies
COPY requirements-api.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --no-cache-dir pip-tools && \
    for i in {1..3}; do \
    	pip install --no-cache-dir -r requirements-api.txt && break || \
        echo "Retry attempt $i" && sleep 5; \
    done

RUN useradd user

USER user

ENV HOME=/home/user \
    PATH=$HOME/.local/bin:$PATH

WORKDIR $HOME/backend

# Create necessary directories and download ONNX model
RUN mkdir -p $HOME/backend/data/chroma $HOME/backend/data/uploads $HOME/.cache/chroma $HOME/.cache/chroma/onnx_models/all-MiniLM-L6-v2 $HOME/backend/chatbotApp_logs && \
    axel -n 30 https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz \
    -o $HOME/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz && \
    tar xzf $HOME/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz

# Copy application code
COPY --chown=user . $HOME/backend

# Set environment variables
ENV PYTHONPATH=$HOME/backend:$HOME/backend/app
ENV PYTHONUNBUFFERED=1
ENV DOCKER_BUILDKIT=1
ENV COMPOSE_HTTP_TIMEOUT=300
ENV COMPOSE_BAKE=true
ENV CHROMA_SERVER_HTTP_TIMEOUT=300
ENV UVICORN_TIMEOUT=300
ENV CHROMA_CACHE_DIR=/backend/.cache/chroma
ENV STREAMLIT_SERVER_MAX_UPLOAD_SIZE=2000
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Mount secret at build time
RUN --mount=type=secret,id=GEMINI_API_KEY \
    if [ -f "/run/secrets/GEMINI_API_KEY" ]; then \
    export GEMINI_API_KEY=$(cat /run/secrets/GEMINI_API_KEY); \
    fi

# Set environment variable to read from container's environment
ENV GEMINI_API_KEY=${GEMINI_API_KEY}

# Expose ports for FastAPI and Streamlit
EXPOSE 7860

# Create startup script
RUN echo '''#!/bin/bash\n\
streamlit run main.py --server.port 7860 --server.address 0.0.0.0 --server.enableCORS true --server.enableXsrfProtection true & \n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 300 --reload & \n\
wait''' > ./start.sh && chmod +x ./start.sh

# Commands
CMD ["./start.sh"]
