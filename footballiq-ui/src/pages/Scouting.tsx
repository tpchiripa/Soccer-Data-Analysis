import { useState } from "react";
import api from "../api/api";

interface ScoutResult {
  player_api_id: number;
  player_name: string;
  overall_rating: number;
  potential: number;
  preferred_foot: string;
  height: number;
  weight: number;
}

export default function Scouting() {
  const [minOverall, setMinOverall] = useState("");
  const [minPotential, setMinPotential] = useState("");
  const [preferredFoot, setPreferredFoot] = useState("");
  const [results, setResults] = useState<ScoutResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runScout() {
    setLoading(true);
    setError("");

    const params = new URLSearchParams();
    if (minOverall) params.set("min_overall", minOverall);
    if (minPotential) params.set("min_potential", minPotential);
    if (preferredFoot) params.set("preferred_foot", preferredFoot);
    params.set("limit", "20");

    try {
      const response = await api.get(`/scouting/?${params.toString()}`);
      setResults(response.data);
    } catch (err) {
      console.error("Scouting search failed:", err);
      setError("Search failed. Try different filters.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  async function addToWatchlist(playerApiId: number) {
    try {
      await api.post(`/watchlist/${playerApiId}`);
    } catch (err) {
      console.error("Failed to add to watchlist:", err);
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold text-white">Scouting</h1>
      <p className="text-slate-400 mt-2">
        Discover players using advanced filters.
      </p>

      <div className="mt-8 flex flex-wrap gap-4 items-end">
        <div>
          <label className="block text-sm text-slate-400 mb-1">
            Min Overall
          </label>
          <input
            type="number"
            value={minOverall}
            onChange={(e) => setMinOverall(e.target.value)}
            className="bg-slate-800 text-white px-3 py-2 rounded w-32"
            placeholder="e.g. 85"
          />
        </div>

        <div>
          <label className="block text-sm text-slate-400 mb-1">
            Min Potential
          </label>
          <input
            type="number"
            value={minPotential}
            onChange={(e) => setMinPotential(e.target.value)}
            className="bg-slate-800 text-white px-3 py-2 rounded w-32"
            placeholder="e.g. 85"
          />
        </div>

        <div>
          <label className="block text-sm text-slate-400 mb-1">
            Preferred Foot
          </label>
          <select
            value={preferredFoot}
            onChange={(e) => setPreferredFoot(e.target.value)}
            className="bg-slate-800 text-white px-3 py-2 rounded w-32"
          >
            <option value="">Any</option>
            <option value="left">Left</option>
            <option value="right">Right</option>
          </select>
        </div>

        <button
          onClick={runScout}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {error && <p className="text-red-400 mt-4">{error}</p>}

      <div className="mt-8">
        {results.length === 0 ? (
          <p className="text-slate-400">
            No results yet. Set filters and click Search.
          </p>
        ) : (
          <table className="w-full text-left text-sm text-slate-300">
            <thead>
              <tr className="border-b border-slate-700 text-slate-400">
                <th className="py-2 pr-4">Name</th>
                <th className="py-2 pr-4">Overall</th>
                <th className="py-2 pr-4">Potential</th>
                <th className="py-2 pr-4">Foot</th>
                <th className="py-2 pr-4">Height</th>
                <th className="py-2 pr-4">Weight</th>
                <th className="py-2 pr-4"></th>
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
                  <td className="py-2 pr-4">{player.preferred_foot}</td>
                  <td className="py-2 pr-4">{player.height} cm</td>
                  <td className="py-2 pr-4">{player.weight} kg</td>
                  <td className="py-2 pr-4">
                    <button
                      onClick={() => addToWatchlist(player.player_api_id)}
                      className="text-blue-400 hover:text-blue-300 text-xs"
                    >
                      + Watchlist
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