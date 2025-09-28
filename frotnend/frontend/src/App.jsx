import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import Visualization from "./components/Visualization";
import "./styles.css";

export default function App() {
  const [data, setData] = useState(null);

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <h1>🐦 Bird Audio Viz</h1>
        <nav>
          <a href="#">Home</a>
          <a href="#">Docs</a>
          <a href="#">About</a>
        </nav>
      </header>

      {/* Main content */}
 <main className="main">
  <div className="content-row">
    {/* Left: Upload form */}
    <div className="card upload-card">
      <UploadForm onUploaded={setData} />
    </div>

    {/* Right: Visualization */}
    <div className="visualization-card">
      {data ? (
        <Visualization
          data={data}
          audioUrl={`http://localhost:8000${data.audio_file}`}
          spectrogramUrl={`http://localhost:8000${data.spectrogram_image}`}
          videoUrl={`http://localhost:8000${data.embedding_video}`}
        />
      ) : (
        <p className="placeholder">Upload an audio file to get started.</p>
      )}
    </div>
  </div>
</main>


      {/* Footer */}
      <footer className="footer">
        <p>© {new Date().getFullYear()} Bird Audio Viz</p>
        <p>
          Built with <span className="highlight">React + FastAPI</span>
        </p>
      </footer>
    </div>
  );
}
