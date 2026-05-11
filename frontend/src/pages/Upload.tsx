import { useState } from "react";
import { api } from "../api/client";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const res = await api.post("/upload", formData);

      navigate(`/document/${res.data.id}`);
    } catch {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[90vh] flex items-center justify-center bg-gradient-to-br from-slate-950 via-gray-900 to-black px-6">

      <div className="w-full max-w-xl bg-white/10 backdrop-blur-xl border border-white/20 shadow-2xl rounded-3xl p-10">

        <h1 className="text-4xl font-bold text-white mb-3">
          AI Document Processing
        </h1>

        <p className="text-gray-300 mb-8">
          Upload and process documents instantly
        </p>

        <div className="border-2 border-dashed border-gray-500 rounded-2xl p-10 text-center bg-white/5">

          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="text-white mb-4"
          />

          {file && (
            <p className="text-green-400 mb-4">
              Selected: {file.name}
            </p>
          )}

          <button
            onClick={uploadFile}
            disabled={loading}
            className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:scale-105 transition-transform px-8 py-3 rounded-xl font-semibold text-white shadow-lg"
          >
            {loading ? "Uploading..." : "Upload Document"}
          </button>

        </div>
      </div>
    </div>
  );
}