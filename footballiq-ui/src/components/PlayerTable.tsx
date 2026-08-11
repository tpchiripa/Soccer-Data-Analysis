import { Player } from "../types/Player";

interface Props {
  players: Player[];
}

export default function PlayerTable({ players }: Props) {
  return (
    <table className="w-full mt-6 border-collapse">
      <thead>
        <tr className="bg-slate-800 text-white">
          <th className="p-3 text-left">Player</th>
          <th className="p-3">Age</th>
          <th className="p-3">Position</th>
          <th className="p-3">Nationality</th>
          <th className="p-3">Overall</th>
        </tr>
      </thead>

      <tbody>
        {players.map((player) => (
          <tr
            key={player.id}
            className="border-b border-slate-700 hover:bg-slate-800"
          >
            <td className="p-3">{player.player_name}</td>
            <td className="text-center">{player.age}</td>
            <td className="text-center">{player.preferred_position}</td>
            <td className="text-center">{player.nationality}</td>
            <td className="text-center font-bold">
              {player.overall_rating}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}