# # # app/main.py
# # import numpy as np
# # import librosa
# # from fastapi import FastAPI, UploadFile, File
# # from fastapi.responses import JSONResponse
# # from tensorflow.keras.models import load_model
# # import io
# # import soundfile as sf

# # app = FastAPI()
# # model = load_model("app/instrument_model.h5")

# # def extract_mfcc(file_data, sr=22050, n_mfcc=13):
# #     audio, _ = sf.read(io.BytesIO(file_data))
# #     audio = librosa.to_mono(audio.T if audio.ndim > 1 else audio)
# #     mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
# #     mfcc = mfcc[..., np.newaxis]
# #     mfcc = np.expand_dims(mfcc, axis=0)
# #     return mfcc

# # @app.post("/predict-instrument/")
# # async def predict_instrument(file: UploadFile = File(...)):
# #     audio_bytes = await file.read()
# #     try:
# #         mfcc = extract_mfcc(audio_bytes)
# #         prediction = model.predict(mfcc)
# #         predicted_label = np.argmax(prediction)
# #         labels = ["cel", "cla", "flu", "gac", "gel", "org", "pia", "sax", "tru", "vio", "voi"]
# #         return JSONResponse({"instrument": labels[predicted_label]})
# #     except Exception as e:
# #         return JSONResponse(status_code=500, content={"error": str(e)})

# # app/main.py
# # import numpy as np
# # import librosa
# # from fastapi import FastAPI, UploadFile, File
# # from fastapi.responses import JSONResponse
# # from tensorflow.keras.models import load_model
# # import shutil
# # import soundfile as sf
# # import os

# # app = FastAPI()
# # model = load_model("app/instrument_model.h5")
# # labels = ["cel", "cla", "flu", "gac", "gel", "org", "pia", "sax", "tru", "vio", "voi"]

# # def extract_mfcc(file_path, sr=22050, n_mfcc=13, max_len=1300):
# #     audio, _ = librosa.load(file_path, sr=sr, mono=True)
# #     mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)

# #     # Pad or truncate to max_len
# #     if mfcc.shape[1] < max_len:
# #         pad_width = max_len - mfcc.shape[1]
# #         mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
# #     else:
# #         mfcc = mfcc[:, :max_len]

# #     return mfcc

# # @app.post("/predict-instrument/")
# # async def predict_instrument(file: UploadFile = File(...)):
# #     temp_filename = "temp.wav"
# #     try:
# #         with open(temp_filename, "wb") as buffer:
# #             shutil.copyfileobj(file.file, buffer)

# #         mfcc = extract_mfcc(temp_filename, n_mfcc=13, max_len=1300)
# #         mfcc_flat = mfcc.flatten().reshape(1, -1)

# #         prediction = model.predict(mfcc_flat)[0]  # Shape: (11,)
# #         instrument_probs = {label: float(score) for label, score in zip(labels, prediction)}

# #         return JSONResponse({"instruments": instrument_probs})
# #     except Exception as e:
# #         return JSONResponse(status_code=500, content={"error": str(e)})
# #     finally:
# #         if os.path.exists(temp_filename):
# #             os.remove(temp_filename)


# import numpy as np
# import librosa
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse
# from tensorflow.keras.models import load_model
# import shutil
# import soundfile as sf
# import os

# app = FastAPI()

# # Load model
# model = load_model("app/instrument_model.h5")

# # Label mappings
# labels = ["cel", "cla", "flu", "gac", "gel", "org", "pia", "sax", "tru", "vio", "voi"]
# full_labels = {
#     "cel": "Cello",
#     "cla": "Clarinet",
#     "flu": "Flute",
#     "gac": "Acoustic Guitar",
#     "gel": "Electric Guitar",
#     "org": "Organ",
#     "pia": "Piano",
#     "sax": "Saxophone",
#     "tru": "Trumpet",
#     "vio": "Violin",
#     "voi": "Voice"
# }

# # Feature extraction
# def extract_mfcc(file_path, sr=22050, n_mfcc=13, max_len=1300):
#     audio, _ = librosa.load(file_path, sr=sr, mono=True)
#     mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)

#     if mfcc.shape[1] < max_len:
#         pad_width = max_len - mfcc.shape[1]
#         mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
#     else:
#         mfcc = mfcc[:, :max_len]

#     return mfcc

# # Prediction endpoint
# @app.post("/predict-instrument/")
# async def predict_instrument(file: UploadFile = File(...)):
#     temp_filename = "temp.wav"
#     try:
#         with open(temp_filename, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         mfcc = extract_mfcc(temp_filename, n_mfcc=13, max_len=1300)
#         mfcc_flat = mfcc.flatten().reshape(1, -1)

#         prediction = model.predict(mfcc_flat)[0]  # Shape: (11,)

#         # Set confidence threshold
#         threshold = 0.10

#         # Filter instruments with confidence above the threshold
#         filtered_probs = {
#             full_labels[label]: float(score)
#             for label, score in zip(labels, prediction)
#             if score >= threshold
#         }

#         return JSONResponse({"instruments": filtered_probs})
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
#     finally:
#         if os.path.exists(temp_filename):
#             os.remove(temp_filename)
import numpy as np
import librosa
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
import shutil
import soundfile as sf
import os

app = FastAPI()

# Get path relative to this file (inside services/instrument-api)
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "instrument_model.h5")

# Load model
model = load_model(MODEL_PATH)

# Label mappings
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

# Feature extraction
def extract_mfcc(file_path, sr=22050, n_mfcc=13, max_len=1300):
    audio, _ = librosa.load(file_path, sr=sr, mono=True)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)

    if mfcc.shape[1] < max_len:
        pad_width = max_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_len]

    return mfcc

# Prediction endpoint
@app.post("/predict-instrument/")
async def predict_instrument(file: UploadFile = File(...)):
    temp_filename = "temp.wav"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        mfcc = extract_mfcc(temp_filename, n_mfcc=13, max_len=1300)
        mfcc_flat = mfcc.flatten().reshape(1, -1)

        prediction = model.predict(mfcc_flat)[0]  # Shape: (11,)

        # Set confidence threshold
        threshold = 0.10

        # Filter instruments with confidence above the threshold
        filtered_probs = {
            full_labels[label]: float(score)
            for label, score in zip(labels, prediction)
            if score >= threshold
        }

        return JSONResponse({"instruments": filtered_probs})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
