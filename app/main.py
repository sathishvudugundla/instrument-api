# from fastapi import FastAPI, UploadFile, File
# from keras.models import load_model

# app = FastAPI()
# model = None

# @app.get("/")
# async def read_root():
#     return {"status": "running"}

# @app.post("/predict/")
# async def predict(file: UploadFile = File(...)):
#     global model
#     if model is None:
#         model = load_model("app/instrument_model.h5")
#     return {"result": "prediction logic here"}

from fastapi import FastAPI, UploadFile, File
import numpy as np
import librosa
from tensorflow.keras.models import load_model

app = FastAPI()

model = None

def get_model():
    global model
    if model is None:
        model = load_model("app/instrument_model.h5")
    return model

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()

    # Save temp file
    with open("temp.wav", "wb") as f:
        f.write(contents)

    # Load and preprocess the audio
    y, sr = librosa.load("temp.wav", sr=None)  # Auto-detect sample rate
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    padded_mfccs = np.zeros((40, 216))  # Or adjust depending on model input shape
    padded_mfccs[:, :min(mfccs.shape[1], 216)] = mfccs[:, :min(mfccs.shape[1], 216)]
    padded_mfccs = np.expand_dims(padded_mfccs, axis=0)

    # Get model prediction
    model = get_model()
    prediction = model.predict(padded_mfccs)
    predicted_label = int(np.argmax(prediction))

    return {"result": predicted_label}
