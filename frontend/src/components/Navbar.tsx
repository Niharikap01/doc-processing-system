import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="backdrop-blur-xl bg-white/10 border-b border-white/10 px-6 py-4 flex justify-between items-center shadow-lg">

      <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
        DocAI
      </h1>

      <div className="space-x-6 text-sm">
        <Link to="/upload" className="hover:text-blue-400">
          Upload
        </Link>
        <Link to="/dashboard" className="hover:text-purple-400">
          Dashboard
        </Link>
      </div>
    </div>
  );
}