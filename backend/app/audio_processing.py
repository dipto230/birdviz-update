import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import umap.umap_ as umap
from matplotlib import animation

def process_audio_file(in_path, out_dir, n_mfcc=40, hop_length=512):
    y, sr = librosa.load(in_path, sr=None)

    # MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, hop_length=hop_length)
    frames = mfcc.shape[1]
    times = librosa.frames_to_time(np.arange(frames), sr=sr, hop_length=hop_length)

    # Spectral features
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=hop_length)[0]
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=hop_length)
    flatness = librosa.feature.spectral_flatness(y=y, hop_length=hop_length)[0]
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop_length)[0]

    # Feature matrix
    extra = np.vstack([centroid, bandwidth, flatness, zcr])
    features = np.hstack([mfcc.T, extra.T])

    # 3D embedding
    reducer = umap.UMAP(n_components=3, random_state=42)
    embedding = reducer.fit_transform(features)

    # Save mel-spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length)
    S_db = librosa.power_to_db(S, ref=np.max)

    plt.figure(figsize=(9, 3.2))
    librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis="time", y_axis="mel")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Mel spectrogram")
    fname = os.path.splitext(os.path.basename(in_path))[0]
    img_name = f"{fname}_mel.png"
    img_path = os.path.join(out_dir, img_name)
    plt.savefig(img_path, bbox_inches="tight", dpi=150)
    plt.close()

    # Save 3D animation
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")
    scat = ax.scatter(
        embedding[:, 0],
        embedding[:, 1],
        embedding[:, 2],
        c=np.linspace(0, 1, embedding.shape[0]),
        cmap="viridis",
        s=15,
    )

    def init():
        ax.view_init(elev=20, azim=30)
        return scat,

    def animate(i):
        ax.view_init(elev=20, azim=i)
        return scat,

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=360, interval=30, blit=True)
    video_name = f"{fname}_3d.mp4"
    video_path = os.path.join(out_dir, video_name)
    anim.save(video_path, fps=30, extra_args=["-vcodec", "libx264"])
    plt.close()

    return {
        "sr": int(sr),
        "times": times.tolist(),
        "mfcc": mfcc.tolist(),
        "embedding": embedding.tolist(),
        "spectral_centroid": centroid.tolist(),
        "spectral_bandwidth": bandwidth.tolist(),
        "spectral_contrast": contrast.tolist(),
        "spectral_flatness": flatness.tolist(),
        "zcr": zcr.tolist(),
        "spectrogram_image": f"/static/outputs/{img_name}",
        "embedding_video": f"/static/outputs/{video_name}",
        "audio_file": f"/static/uploads/{os.path.basename(in_path)}"
    }
