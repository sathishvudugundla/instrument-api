FROM python:3.10-slim

# Install required system packages for librosa and TensorFlow
RUN apt-get update && apt-get install -y \
    ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
COPY . .

# Install uv tool to sync, OR use pip if uv is not needed
RUN pip install --upgrade pip && pip install uvicorn[standard] fastapi librosa numpy tensorflow python-multipart pydantic

CMD ["uvicorn", "services.instrument_api.main:app", "--host", "0.0.0.0", "--port", "80"]
