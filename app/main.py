from fastapi import FastAPI, UploadFile, File
from keras.models import load_model

app = FastAPI()
model = None

@app.get("/")
async def read_root():
    return {"status": "running"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    global model
    if model is None:
        model = load_model("app/instrument_model.h5")
    return {"result": "prediction logic here"}