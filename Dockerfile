FROM python:3.11-slim

# System dependencies for sentence-transformers and chromadb
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies first (for Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create the vectorstore directory (ChromaDB will populate at startup)
RUN mkdir -p data/vectorstore data/documents

# Expose port
EXPOSE 8000

# Run the ingestion script then start the server
CMD python scripts/ingest.py && uvicorn main:app --host 0.0.0.0 --port 8000
