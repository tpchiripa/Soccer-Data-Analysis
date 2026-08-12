// Matches the response shape from GET /players/search and /players/top.
// Fields not yet returned by the backend are marked optional so the UI
// degrades gracefully instead of crashing when they're absent.
export interface Player {
  player_api_id: number;
  player_name: string;
  overall_rating: number;
  potential: number;
  age: number;

  // Not yet present in this dataset — see /players/routers/players.py
  // and player_service.py for what's actually returned.
  preferred_position?: string;
  nationality?: string;
}