// components/UploadForm.jsx
import React, { useState } from "react";
import axios from "axios";

export default function UploadForm({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Choose a file first");

    setLoading(true);
    const fd = new FormData();
    fd.append("file", file);

    try {
      const resp = await axios.post("http://localhost:8000/process", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      onUploaded(resp.data);
    } catch (err) {
      alert("Upload failed: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-xl shadow-md w-full mb-8 flex flex-col gap-4"
    >
      <label className="text-sm font-medium text-gray-700">
        Upload an audio file
      </label>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="block w-full text-sm text-gray-600 border border-gray-300 rounded-md p-2"
      />
      <button
        type="submit"
        disabled={loading}
        className={`px-4 py-2 rounded-md text-white font-medium transition ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-indigo-600 hover:bg-indigo-700"
        }`}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </form>
  );
}
