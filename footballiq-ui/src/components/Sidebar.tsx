import {
  Home,
  Users,
  Search,
  GitCompare,
  BrainCircuit,
  Star,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const menu = [
  {
    icon: Home,
    label: "Dashboard",
    path: "/",
  },
  {
    icon: Users,
    label: "Players",
    path: "/players",
  },
  {
    icon: Search,
    label: "Scouting",
    path: "/scouting",
  },
  {
    icon: BrainCircuit,
    label: "Similarity",
    path: "/similarity",
  },
  {
    icon: GitCompare,
    label: "Comparison",
    path: "/comparison",
  },
  {
    icon: Star,
    label: "Watchlist",
    path: "/watchlist",
  },
];

export default function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-slate-950 text-white p-6">
      <h1 className="text-2xl font-bold mb-10">FootballIQ</h1>
      <nav className="space-y-3">
        {menu.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.label}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `flex items-center gap-3 p-3 rounded-lg transition ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "hover:bg-slate-800 text-slate-300"
                }`
              }
            >
              <Icon size={20} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}