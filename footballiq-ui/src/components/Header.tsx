import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const initial = user?.email?.charAt(0).toUpperCase() ?? "?";

  return (
    <header className="bg-slate-900/80 backdrop-blur border-b border-slate-800 px-8 py-5 flex justify-between items-center sticky top-0 z-10">
      <div>
        <h2 className="text-xl font-semibold text-white">Dashboard</h2>
        <p className="text-slate-500 text-sm">Football Analytics Platform</p>
      </div>

      <div className="flex items-center gap-3">
        <div className="text-right">
          <p className="text-sm font-medium text-white">
            {user?.email ?? "Guest"}
          </p>
          <button
            onClick={handleLogout}
            className="text-xs text-slate-500 hover:text-red-400 transition"
          >
            Sign out
          </button>
        </div>
        <div className="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-semibold">
          {initial}
        </div>
      </div>
    </header>
  );
}