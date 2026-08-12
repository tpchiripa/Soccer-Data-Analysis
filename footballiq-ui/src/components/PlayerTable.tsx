import type { Player } from "../types/Player";

interface PlayerTableProps {
  players: Player[];
}

export default function PlayerTable({ players }: PlayerTableProps) {
  if (players.length === 0) {
    return (
      <p className="text-slate-400">
        No players to show. Try a different search.
      </p>
    );
  }

  return (
    <table className="w-full text-left text-sm text-slate-300">
      <thead>
        <tr className="border-b border-slate-700 text-slate-400">
          <th className="py-2 pr-4">Name</th>
          <th className="py-2 pr-4">Overall</th>
          <th className="py-2 pr-4">Potential</th>
          <th className="py-2 pr-4">Position</th>
          <th className="py-2 pr-4">Nationality</th>
          <th className="py-2 pr-4">Age</th>
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
            <td className="py-2 pr-4">{player.preferred_position ?? "N/A"}</td>
            <td className="py-2 pr-4">{player.nationality ?? "N/A"}</td>
            <td className="py-2 pr-4">{player.age ?? "N/A"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}