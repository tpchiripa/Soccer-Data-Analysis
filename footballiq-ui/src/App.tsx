import { BrowserRouter, Routes, Route } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";

import Dashboard from "./pages/Dashboard";
import Players from "./pages/Players";
import Similarity from "./pages/Similarity";
import Comparison from "./pages/Comparison";
import Scouting from "./pages/Scouting";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/players" element={<Players />} />
          <Route path="/similarity" element={<Similarity />} />
          <Route path="/comparison" element={<Comparison />} />
          <Route path="/scouting" element={<Scouting />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;