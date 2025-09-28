// components/Visualization.jsx
import React, { useEffect, useRef } from "react";
import Plotly from "plotly.js-basic-dist";

function nearestIndex(times, t) {
  let lo = 0,
    hi = times.length - 1;
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    if (times[mid] < t) lo = mid + 1;
    else hi = mid;
  }
  return lo;
}

export default function Visualization({ data, audioUrl, spectrogramUrl, videoUrl }) {
  const plotRef = useRef(null);
  const audioRef = useRef(null);

  // Plotly 3D scatter plot
  useEffect(() => {
    if (!data) return;
    const emb = data.embedding;
    const times = data.times;

    const xs = emb.map((e) => e[0]);
    const ys = emb.map((e) => e[1]);
    const zs = emb.map((e) => e[2]);

    const trace = {
      x: xs,
      y: ys,
      z: zs,
      mode: "markers",
      type: "scatter3d",
      marker: {
        size: 3,
        color: times,
        colorscale: "Jet",
        colorbar: { title: "time (s)" },
      },
    };

    const layout = {
      margin: { l: 0, r: 0, b: 0, t: 0 },
      scene: { aspectmode: "auto" },
    };

    Plotly.newPlot(plotRef.current, [trace], layout, { responsive: true });
  }, [data]);

  // Sync audio playback with Plotly markers
  useEffect(() => {
    if (!audioRef.current || !data) return;
    const times = data.times;
    const n = times.length;
    const baseSizes = new Array(n).fill(3);

    const onTime = () => {
      const t = audioRef.current.currentTime;
      const idx = nearestIndex(times, t);
      const sizes = baseSizes.slice();
      sizes[idx] = 10;
      Plotly.restyle(plotRef.current, { "marker.size": [sizes] });
    };

    audioRef.current.addEventListener("timeupdate", onTime);
    return () => audioRef.current.removeEventListener("timeupdate", onTime);
  }, [data]);

  return (
    <div className="flex flex-col gap-6">
      {/* Row 1: 3D Graph + Spectrogram */}
      <div className="flex flex-row gap-6 items-start">
        {/* Left: 3D Plot */}
        <div className="bg-white rounded-xl shadow-md p-4 flex-1">
          <div ref={plotRef} style={{ height: 500 }} />
        </div>

        {/* Right: Spectrogram */}
        <div className="bg-white rounded-xl shadow-md overflow-hidden flex-1">
          <img
            src={spectrogramUrl}
            alt="spectrogram"
            className="w-full h-full object-contain"
          />
        </div>
      </div>

      {/* Row 2: Audio + Video + Tip */}
      <div className="flex flex-col gap-4">
        <audio ref={audioRef} controls src={audioUrl} className="w-full" />
        <video controls src={videoUrl} className="w-full rounded-md shadow-md" />
        <p className="text-sm text-gray-500">
          💡 Tip: Play audio and watch the 3D embedding highlight the current frame.
        </p>
      </div>
    </div>
  );
}
