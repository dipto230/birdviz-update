import os
import uuid
import json
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .audio_processing import process_audio_file

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = STATIC_DIR / "uploads"
OUTPUTS_DIR = STATIC_DIR / "outputs"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Bird Audio Viz API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def root():
    return {"ok": True, "note": "POST audio file to /upload"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # basic content-type check (allow common audio)
    if not file.filename:
        raise HTTPException(status_code=400, detail="no filename")
    # save uploaded file
    ext = Path(file.filename).suffix or ".wav"
    filename = f"{uuid.uuid4().hex}{ext}"
    target_path = UPLOADS_DIR / filename
    contents = await file.read()
    with open(target_path, "wb") as f:
        f.write(contents)

    # process
    try:
        result = process_audio_file(str(target_path), str(OUTPUTS_DIR))
    except Exception as e:
        # cleanup on error
        raise HTTPException(status_code=500, detail=f"processing failed: {e}")

    # persist JSON
    json_name = f"{Path(filename).stem}.json"
    json_path = OUTPUTS_DIR / json_name
    # add full URLs for client convenience
    result['audio_url'] = f"/static/uploads/{filename}"
    result['spectrogram_url'] = f"/static/outputs/{result['spectrogram_image']}"
    result['embedding_video_url'] = f"/static/outputs/{result['embedding_video']}"

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(result, jf)

    return {"json_url": f"/static/outputs/{json_name}", "audio_url": result['audio_url'], "spectrogram_url": result['spectrogram_url']}
