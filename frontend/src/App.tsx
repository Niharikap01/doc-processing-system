import { Routes, Route, Navigate } from "react-router-dom";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import DocumentDetail from "./pages/DocumentDetail";
import Navbar from "./components/Navbar";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 text-white">
      <Navbar />

      <div className="flex justify-center px-4 py-6">
        <div className="w-full max-w-5xl">

          <Routes>
            <Route path="/" element={<Navigate to="/upload" />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/document/:id" element={<DocumentDetail />} />
          </Routes>

        </div>
      </div>

    </div>
  );
}

export default App;