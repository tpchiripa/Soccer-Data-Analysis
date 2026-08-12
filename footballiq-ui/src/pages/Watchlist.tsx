import { useEffect, useState } from "react";
import api from "../api/api";

interface WatchlistPlayer {
  player_api_id: number;
  player_name: string;
  overall_rating: number;
  potential: number;
  note: string;
  added_at: string;
}

export default function Watchlist() {
  const [players, setPlayers] = useState<WatchlistPlayer[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadWatchlist() {
    setLoading(true);
    try {
      const response = await api.get("/watchlist/");
      setPlayers(response.data);
    } catch (err) {
      console.error("Failed to load watchlist:", err);
    } finally {
      setLoading(false);
    }
  }

  async function removePlayer(playerApiId: number) {
    try {
      await api.delete(`/watchlist/${playerApiId}`);
      setPlayers((prev) =>
        prev.filter((p) => p.player_api_id !== playerApiId)
      );
    } catch (err) {
      console.error("Failed to remove player:", err);
    }
  }

  useEffect(() => {
    loadWatchlist();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold text-white">Watchlist</h1>
      <p className="text-slate-400 mt-2">
        Players you're tracking for call-ups or transfer targets.
      </p>

      <div className="mt-8">
        {loading ? (
          <p className="text-slate-400">Loading...</p>
        ) : players.length === 0 ? (
          <p className="text-slate-400">
            No players on your watchlist yet. Add some from Players or
            Scouting.
          </p>
        ) : (
          <table className="w-full text-left text-sm text-slate-300">
            <thead>
              <tr className="border-b border-slate-700 text-slate-400">
                <th className="py-2 pr-4">Name</th>
                <th className="py-2 pr-4">Overall</th>
                <th className="py-2 pr-4">Potential</th>
                <th className="py-2 pr-4">Note</th>
                <th className="py-2 pr-4">Added</th>
                <th className="py-2 pr-4"></th>
              </tr>
            </thead>
            <tbody>
              {players.map((player) => (
                <tr
                  key={player.player_api_id}
                  className="border-b border-slate-800 hover:bg-slate-800/50"
                >
                  <td className="py-2 pr-4 font-medium text-white">
                    {player.player_name}
                  </td>
                  <td className="py-2 pr-4">{player.overall_rating}</td>
                  <td className="py-2 pr-4">{player.potential}</td>
                  <td className="py-2 pr-4">{player.note || "-"}</td>
                  <td className="py-2 pr-4">
                    {new Date(player.added_at).toLocaleDateString()}
                  </td>
                  <td className="py-2 pr-4">
                    <button
                      onClick={() => removePlayer(player.player_api_id)}
                      className="text-red-400 hover:text-red-300"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}