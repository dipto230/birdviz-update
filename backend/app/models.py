from pydantic import BaseModel
from typing import List

class ProcessResult(BaseModel):
    sr: int
    times: List[float]
    mfcc: List[List[float]]
    embedding: List[List[float]]
    spectral_centroid: List[float]
    spectral_bandwidth: List[float]
    spectral_contrast: List[List[float]]
    spectral_flatness: List[float]
    zcr: List[float]
    spectrogram_image: str
    embedding_video: str
    audio_file: str
