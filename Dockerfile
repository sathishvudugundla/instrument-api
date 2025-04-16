# Dockerfile
# FROM python:3.10

# WORKDIR /app

# COPY ./requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

# COPY ./app ./app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# tempory changes

# FROM python:3.10

# WORKDIR /app

# # Copy requirements and install dependencies
# COPY ./requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Copy the app directory
# COPY ./app ./app

# # Expose the port your FastAPI app is running on
# EXPOSE 8000

# # Start FastAPI app using uvicorn
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Dockerfile
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
COPY services/ ./services/

RUN uv sync --no-dev

EXPOSE 8000
CMD ["uv", "run", "services/instrument-api/main.py"]
