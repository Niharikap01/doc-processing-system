import { useEffect, useState } from "react";

export function useWebSocket(docId: number) {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (!docId) return;

    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${docId}`);

    ws.onmessage = (event) => {
      setData(JSON.parse(event.data));
    };

    ws.onerror = (err) => {
      console.log("WebSocket error", err);
    };

    return () => ws.close();
  }, [docId]);

  return data;
}