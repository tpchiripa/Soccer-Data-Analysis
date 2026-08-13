import { useEffect, useState } from "react";
import api from "../api/api";
import DashboardCard from "../components/DashboardCard";
import SearchBox from "../components/SearchBox";
import { useAuth } from "../context/AuthContext";

interface DashboardStats {
  players: number;
  watchlist_count: number;
  top_player: {
    player_name: string;
    overall_rating: number;
  } | null;
}

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/dashboard/stats")
      .then((response) => {
        setStats(response.data);
      })
      .catch((error) => {
        console.error("Failed to load dashboard statistics:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold text-white">
        Welcome back, {user?.email?.split("@")[0] ?? "Admin"}
      </h1>
      <p className="mt-2 text-slate-400">
        Here's what's happening across FootballIQ.
      </p>

      {loading ? (
        <div className="grid grid-cols-1 gap-6 mt-10 md:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50 animate-pulse h-24"
            />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 mt-10 md:grid-cols-3">
          <DashboardCard
            title="Players in Database"
            value={stats?.players.toLocaleString() ?? "0"}
          />
          <DashboardCard
            title="On Your Watchlist"
            value={stats?.watchlist_count.toString() ?? "0"}
            color="bg-blue-900/40"
          />
          <DashboardCard
            title="Top Rated Player"
            value={stats?.top_player?.player_name ?? "N/A"}
            subtitle={
              stats?.top_player
                ? `Overall: ${stats.top_player.overall_rating}`
                : undefined
            }
            color="bg-emerald-900/40"
          />
        </div>
      )}

      <div className="mt-10">
        <h3 className="text-lg font-semibold text-white mb-4">
          Quick Search
        </h3>
        <SearchBox />
      </div>
    </div>
  );
}