import { useState } from "react";
import api from "../api/api";

interface SimilarPlayer {
  player_api_id: number;
  player_name: string;
  overall_rating: number;
  potential: number;
  distance: number;
}

export default function Similarity() {
  const [playerName, setPlayerName] = useState("");
  const [results, setResults] = useState<SimilarPlayer[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function findSimilar() {
    if (!playerName.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await api.get(
        `/similarity/${encodeURIComponent(playerName)}`
      );
      setResults(response.data);
    } catch (err) {
      console.error("Similarity search failed:", err);
      setError(`No player found matching "${playerName}".`);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold text-white">Similarity Engine</h1>
      <p className="text-slate-400 mt-2">
        Find players with similar playing styles.
      </p>

      <div className="mt-8 flex gap-4 items-end">
        <div>
          <label className="block text-sm text-slate-400 mb-1">
            Player Name
          </label>
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && findSimilar()}
            className="bg-slate-800 text-white px-3 py-2 rounded w-64"
            placeholder="e.g. Lionel Messi"
          />
        </div>

        <button
          onClick={findSimilar}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded disabled:opacity-50"
        >
          {loading ? "Searching..." : "Find Similar"}
        </button>
      </div>

      {error && <p className="text-red-400 mt-4">{error}</p>}

      <div className="mt-8">
        {results.length === 0 ? (
          <p className="text-slate-400">
            Enter a player's full name to find similar players.
          </p>
        ) : (
          <table className="w-full text-left text-sm text-slate-300">
            <thead>
              <tr className="border-b border-slate-700 text-slate-400">
                <th className="py-2 pr-4">Name</th>
                <th className="py-2 pr-4">Overall</th>
                <th className="py-2 pr-4">Potential</th>
                <th className="py-2 pr-4">Similarity Distance</th>
              </tr>
            </thead>
            <tbody>
              {results.map((player) => (
                <tr
                  key={player.player_api_id}
                  className="border-b border-slate-800 hover:bg-slate-800/50"
                >
                  <td className="py-2 pr-4 font-medium text-white">
                    {player.player_name}
                  </td>
                  <td className="py-2 pr-4">{player.overall_rating}</td>
                  <td className="py-2 pr-4">{player.potential}</td>
                  <td className="py-2 pr-4">{player.distance.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}