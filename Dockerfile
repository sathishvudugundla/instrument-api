# # Dockerfile
# FROM python:3.10

# WORKDIR /app

# COPY ./requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

# COPY ./app ./app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Use slim base for smaller image, but add system dependencies
# FROM python:3.10-slim

# # Set working directory
# WORKDIR /app

# # Install system dependencies for audio processing
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     libsndfile1 \
#     libglib2.0-0 \
#     libsm6 \
#     libxrender1 \
#     libxext6 \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Copy application files
# COPY ./app ./app

# ENV PORT=10000
# # Run the app
# # CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY ./app ./app

# Default fallback port (in local/dev only)
ENV PORT=8000

# Correct way to run app using shell (so $PORT is interpolated)
ENTRYPOINT sh -c "uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
