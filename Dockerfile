FROM python:3.10-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Add this to help Python resolve package imports
ENV PYTHONPATH=/app

# Copy files
COPY pyproject.toml ./
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install uvicorn[standard] fastapi librosa numpy tensorflow python-multipart pydantic

# Expose port for Restack/HTTP
EXPOSE 80

# Start FastAPI app
CMD ["uvicorn", "services.instrument_api.main:app", "--host", "0.0.0.0", "--port", "80"]
