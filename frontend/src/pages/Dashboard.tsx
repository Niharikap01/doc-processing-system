import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const [docs, setDocs] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/documents")
      .then((res) => res.json())
      .then(setDocs);
  }, []);

  return (
    <div className="p-10">
      <h2 className="text-2xl font-bold mb-6">Dashboard</h2>

      <div className="grid gap-4">
        {docs.map((doc) => (
          <Link
            key={doc.id}
            to={`/document/${doc.id}`}
            className="bg-white/10 backdrop-blur-lg border border-white/10 p-5 rounded-xl hover:scale-[1.02]"
          >
            <p className="font-semibold">{doc.filename}</p>
            <p className="text-sm text-gray-300">
              Status: {doc.status}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}