import { useEffect, useState } from "react";

import api from "../api/api";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import DashboardCard from "../components/DashboardCard";
import SearchBox from "../components/SearchBox";

export default function Dashboard() {
  const [stats, setStats] = useState({
    players: 0,
    similarity_engine: "",
    api_status: "",
  });

  useEffect(() => {
    api
      .get("/dashboard/stats")
      .then((response) => {
        setStats(response.data);
      })
      .catch((error) => {
        console.error("Failed to load dashboard statistics:", error);
      });
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />

      <div className="flex-1">
        <Header />

        <main className="p-8">
          <h1 className="text-4xl font-bold text-white">
            FootballIQ Dashboard
          </h1>

          <p className="mt-2 text-slate-400">
            Enterprise Football Analytics Platform
          </p>

          <div className="grid grid-cols-1 gap-6 mt-10 md:grid-cols-3">
            <DashboardCard
              title="Players"
              value={stats.players.toLocaleString()}
            />

            <DashboardCard
              title="Similarity Engine"
              value={stats.similarity_engine}
              color="bg-green-800"
            />

            <DashboardCard
              title="API Status"
              value={stats.api_status}
              color="bg-blue-800"
            />
          </div>

          <div className="mt-10">
            <SearchBox />
          </div>
        </main>
      </div>
    </div>
  );
}