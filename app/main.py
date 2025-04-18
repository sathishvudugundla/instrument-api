
import numpy as np
import librosa
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
import io
import soundfile as sf

app = FastAPI()
model = load_model("instrument_model.h5")

def extract_mfcc(file_data, sr=22050, n_mfcc=13):
    audio, _ = sf.read(io.BytesIO(file_data))
    audio = librosa.to_mono(audio.T if audio.ndim > 1 else audio)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    mfcc_scaled = np.mean(mfcc.T, axis=0)
    return mfcc_scaled

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        mfccs = extract_mfcc(contents)
        prediction = model.predict(np.expand_dims(mfccs, axis=0))
        predicted_class = int(np.argmax(prediction))
        return JSONResponse(content={"predicted_class": predicted_class})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
