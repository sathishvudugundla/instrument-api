# Dockerfile
# FROM python:3.10

# WORKDIR /app

# COPY ./requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

# COPY ./app ./app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# tempory changes

FROM python:3.10

WORKDIR /app

# Copy requirements and install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the app directory
COPY ./app ./app

# Expose the port your FastAPI app is running on
EXPOSE 8000

# Start FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
