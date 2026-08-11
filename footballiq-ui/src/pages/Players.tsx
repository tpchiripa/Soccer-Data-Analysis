import { useState } from "react";

import api from "../api/api";

import SearchBox from "../components/SearchBox";
import PlayerTable from "../components/PlayerTable";

import { Player } from "../types/Player";

export default function Players() {
  const [players, setPlayers] = useState<Player[]>([]);

  async function searchPlayers(name: string) {
    if (!name.trim()) {
      setPlayers([]);
      return;
    }

    try {
      const response = await api.get(
        `/players/search?name=${encodeURIComponent(name)}`
      );

      setPlayers(response.data);
    } catch (error) {
      console.error("Failed to search players:", error);
      setPlayers([]);
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white">
        Player Search
      </h1>

      <p className="mt-2 text-slate-400">
        Search FootballIQ's player database
      </p>

      <div className="mt-8">
        <SearchBox onSearch={searchPlayers} />
      </div>

      <div className="mt-8">
        <PlayerTable players={players} />
      </div>
    </div>
  );
}