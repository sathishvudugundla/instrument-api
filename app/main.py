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

import numpy as np
import librosa
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
import shutil
import soundfile as sf
import os
import logging


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        # Dummy data to trigger a dry run
        dummy_input = np.zeros((1, 13 * 1300))
        model.predict(dummy_input)
        print("Model warm-up complete.")
    except Exception as e:
        print(f"Error during model warm-up: {e}")
        
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy load model
model = None
labels = ["cel", "cla", "flu", "gac", "gel", "org", "pia", "sax", "tru", "vio", "voi"]
full_labels = {
    "cel": "Cello",
    "cla": "Clarinet",
    "flu": "Flute",
    "gac": "Acoustic Guitar",
    "gel": "Electric Guitar",
    "org": "Organ",
    "pia": "Piano",
    "sax": "Saxophone",
    "tru": "Trumpet",
    "vio": "Violin",
    "voi": "Voice"
}

def get_model():
    global model
    if model is None:
        try:
            model = load_model("app/instrument_model.h5")
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    return model

def extract_mfcc(file_path, sr=22050, n_mfcc=13, max_len=1300):
    audio, _ = librosa.load(file_path, sr=sr, mono=True)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)

    if mfcc.shape[1] < max_len:
        pad_width = max_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_len]

    return mfcc

@app.post("/predict-instrument")
async def predict_instrument(file: UploadFile = File(...)):
    temp_filename = "temp.wav"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        mfcc = extract_mfcc(temp_filename, n_mfcc=13, max_len=1300)
        mfcc_flat = mfcc.flatten().reshape(1, -1)

        model_instance = get_model()
        prediction = model_instance.predict(mfcc_flat)[0]

        threshold = 0.10
        filtered_probs = {
            full_labels[label]: float(score)
            for label, score in zip(labels, prediction)
            if score >= threshold
        }

        return JSONResponse({"instruments": filtered_probs})
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.get("/")
def read_root():
    return {"message": "Instrument classifier is running 🚀"}
