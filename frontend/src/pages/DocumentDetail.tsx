import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

type DocStatus =
  | "queued"
  | "processing"
  | "completed"
  | "failed"
  | "finalized"
  | "job_started"
  | "parsing"
  | "extracting"
  | "saving"
  | "loading";

export default function DocumentDetail() {

  const { id } = useParams();

  const [status, setStatus] =
    useState<DocStatus>("loading");

  const [data, setData] = useState<any>({});

  const [error, setError] = useState("");

  // ---------------- FETCH DATA ----------------

  const fetchDocument = async () => {
    try {

      const statusRes = await fetch(
        `http://127.0.0.1:8000/status/${id}`
      );

      const statusData = await statusRes.json();

      if (statusData.error) {
        setError(statusData.error);
      } else {
        setStatus(statusData.status);
      }

      const docRes = await fetch(
        `http://127.0.0.1:8000/documents/${id}`
      );

      const docData = await docRes.json();

      setData(
        docData.reviewed_data ||
        docData.extracted_data ||
        {}
      );

    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {

    fetchDocument();

    // ---------------- WEBSOCKET ----------------

    const ws = new WebSocket(
      `ws://127.0.0.1:8000/ws/${id}`
    );

    ws.onmessage = (event) => {

      const msg = JSON.parse(event.data);

      console.log("WS MESSAGE:", msg);

      if (msg.status) {
        setStatus(msg.status);
      }

      // reload latest extracted data
      fetchDocument();
    };

    ws.onerror = (err) => {
      console.log("WebSocket Error:", err);
    };

    return () => {
      ws.close();
    };

  }, [id]);

  // ---------------- HANDLE CHANGE ----------------

  const handleChange = (
    key: string,
    value: string
  ) => {

    setData((prev: any) => ({
      ...prev,
      [key]: value,
    }));
  };

  // ---------------- SAVE ----------------

  const saveData = async () => {

    await fetch(
      `http://127.0.0.1:8000/documents/${id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    alert("Saved!");
  };

  // ---------------- FINALIZE ----------------

  const finalizeDocument = async () => {

    await fetch(
      `http://127.0.0.1:8000/documents/${id}/finalize`,
      {
        method: "POST",
      }
    );

    setStatus("finalized");

    alert("Document Finalized");
  };

  // ---------------- EXPORTS ----------------

  const exportJSON = () => {

    window.open(
      `http://127.0.0.1:8000/documents/${id}/export/json`,
      "_blank"
    );
  };

  const exportCSV = () => {

    window.open(
      `http://127.0.0.1:8000/documents/${id}/export/csv`,
      "_blank"
    );
  };

  // ---------------- STATUS BAR ----------------

  const getProgress = () => {

    switch (status) {

      case "queued":
        return 10;

      case "job_started":
        return 20;

      case "parsing":
        return 40;

      case "extracting":
        return 60;

      case "saving":
        return 80;

      case "completed":
      case "finalized":
        return 100;

      default:
        return 0;
    }
  };

  // ---------------- UI ----------------

  return (

    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-gray-900 to-black py-10 px-4 flex justify-center">

      <div className="w-full max-w-4xl bg-white/10 backdrop-blur-xl border border-white/10 shadow-2xl rounded-3xl p-8">

        <h1 className="text-4xl font-bold text-white mb-2">
          Document Dashboard
        </h1>

        <p className="text-gray-400 mb-8">
          Document ID: {id}
        </p>

        {error ? (

          <p className="text-red-400">
            {error}
          </p>

        ) : (

          <>
            {/* STATUS */}

            <div className="mb-8">

              <div className="flex justify-between mb-2">

                <span className="text-gray-300">
                  Processing Status
                </span>

                <span className="text-cyan-400 font-semibold capitalize">
                  {status}
                </span>

              </div>

              <div className="w-full h-4 bg-gray-700 rounded-full overflow-hidden">

                <div
                  className="h-4 bg-gradient-to-r from-cyan-500 to-blue-600 transition-all duration-500"
                  style={{
                    width: `${getProgress()}%`,
                  }}
                />

              </div>

            </div>

            {/* DATA */}

            {Object.keys(data).length === 0 ? (

              <div className="text-center text-gray-400 py-10">
                No extracted data available yet...
              </div>

            ) : (

              <div className="space-y-5">

                {Object.keys(data).map((key) => (

                  <div key={key}>

                    <label className="block text-sm text-gray-300 mb-2 capitalize">

                      {key.replace(/_/g, " ")}

                    </label>

                    <textarea
                      rows={4}
                      value={
                        Array.isArray(data[key])
                          ? data[key].join(", ")
                          : String(data[key] ?? "")
                      }
                      onChange={(e) =>
                        handleChange(key, e.target.value)
                      }
                      className="w-full px-4 py-3 rounded-2xl bg-black/30 border border-white/10 text-white outline-none focus:border-cyan-500 resize-none"
                    />

                  </div>

                ))}

              </div>

            )}

            {/* BUTTONS */}

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-10">

              <button
                onClick={saveData}
                className="bg-gradient-to-r from-green-500 to-emerald-600 py-3 rounded-xl font-semibold hover:scale-105 transition"
              >
                Save
              </button>

              <button
                onClick={finalizeDocument}
                className="bg-gradient-to-r from-purple-500 to-pink-600 py-3 rounded-xl font-semibold hover:scale-105 transition"
              >
                Finalize
              </button>

              <button
                onClick={exportJSON}
                className="bg-gradient-to-r from-blue-500 to-cyan-500 py-3 rounded-xl font-semibold hover:scale-105 transition"
              >
                Export JSON
              </button>

              <button
                onClick={exportCSV}
                className="bg-gradient-to-r from-orange-500 to-yellow-500 py-3 rounded-xl font-semibold hover:scale-105 transition"
              >
                Export CSV
              </button>

            </div>
          </>
        )}
      </div>
    </div>
  );
}