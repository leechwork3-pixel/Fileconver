# /Dockerfile
FROM python:3.10-slim

# Install system dependencies that might be needed by conversion libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Command to run the bot
CMD ["python3", "run.py"]
