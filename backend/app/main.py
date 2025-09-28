import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .audio_processing import process_audio_file
from .models import ProcessResult

# ============================
# Paths
# ============================
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = STATIC_DIR / "uploads"
OUTPUTS_DIR = STATIC_DIR / "outputs"

# Ensure folders exist
for d in [STATIC_DIR, UPLOADS_DIR, OUTPUTS_DIR]:
    os.makedirs(d, exist_ok=True)

# ============================
# FastAPI App
# ============================
app = FastAPI(title="Audio Processing API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ============================
# Routes
# ============================
@app.post("/process", response_model=ProcessResult)
async def process_audio(file: UploadFile = File(...)):
    """Upload and process an audio file."""
    if not file.filename.lower().endswith((".wav", ".mp3", ".flac", ".ogg")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # Save uploaded file
    uid = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    in_path = UPLOADS_DIR / f"{uid}{ext}"
    with open(in_path, "wb") as f:
        f.write(await file.read())

    try:
        result = process_audio_file(str(in_path), str(OUTPUTS_DIR))
        return ProcessResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
