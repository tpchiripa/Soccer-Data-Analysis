import { useState } from "react";
import api from "../api/api";

interface ComparisonRow {
  Attribute: string;
  [playerName: string]: string | number;
}

interface ComparisonResponse {
  comparison: ComparisonRow[];
  top_attributes: ComparisonRow[];
}

export default function Comparison() {
  const [playerOne, setPlayerOne] = useState("");
  const [playerTwo, setPlayerTwo] = useState("");
  const [data, setData] = useState<ComparisonResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function compare() {
    if (!playerOne.trim() || !playerTwo.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await api.get("/comparison/", {
        params: {
          player_one: playerOne,
          player_two: playerTwo,
        },
      });
      setData(response.data);
    } catch (err) {
      console.error("Comparison failed:", err);
      setError("Couldn't compare — check both player names.");
      setData(null);
    } finally {
      setLoading(false);
    }
  }

  function renderTable(rows: ComparisonRow[], title: string) {
    if (rows.length === 0) return null;
    const columns = Object.keys(rows[0]);

    return (
      <div className="mt-8">
        <h2 className="text-xl font-semibold text-white mb-3">{title}</h2>
        <table className="w-full text-left text-sm text-slate-300">
          <thead>
            <tr className="border-b border-slate-700 text-slate-400">
              {columns.map((col) => (
                <th key={col} className="py-2 pr-4">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr
                key={i}
                className="border-b border-slate-800 hover:bg-slate-800/50"
              >
                {columns.map((col) => (
                  <td key={col} className="py-2 pr-4">
                    {row[col]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold text-white">Player Comparison</h1>
      <p className="text-slate-400 mt-2">
        Compare two players side by side.
      </p>

      <div className="mt-8 flex flex-wrap gap-4 items-end">
        <div>
          <label className="block text-sm text-slate-400 mb-1">
            Player One
          </label>
          <input
            type="text"
            value={playerOne}
            onChange={(e) => setPlayerOne(e.target.value)}
            className="bg-slate-800 text-white px-3 py-2 rounded w-56"
            placeholder="e.g. Lionel Messi"
          />
        </div>

        <div>
          <label className="block text-sm text-slate-400 mb-1">
            Player Two
          </label>
          <input
            type="text"
            value={playerTwo}
            onChange={(e) => setPlayerTwo(e.target.value)}
            className="bg-slate-800 text-white px-3 py-2 rounded w-56"
            placeholder="e.g. Cristiano Ronaldo"
          />
        </div>

        <button
          onClick={compare}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded disabled:opacity-50"
        >
          {loading ? "Comparing..." : "Compare"}
        </button>
      </div>

      {error && <p className="text-red-400 mt-4">{error}</p>}

      {data && (
        <>
          {renderTable(data.comparison, "Overview")}
          {renderTable(data.top_attributes, "Top Attributes")}
        </>
      )}
    </div>
  );
}