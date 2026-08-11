import { useState } from "react";

interface SearchBoxProps {
  onSearch: (query: string) => void;
}

export default function SearchBox({ onSearch }: SearchBoxProps) {
  const [query, setQuery] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSearch(query);
  }

  return (
    <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
      <form onSubmit={handleSubmit}>
        <div className="flex gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search player..."
            className="flex-1 bg-slate-900 rounded-lg p-3 text-white outline-none border border-slate-700"
          />

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 px-6 rounded-lg text-white font-semibold transition-colors"
          >
            Search
          </button>
        </div>
      </form>
    </div>
  );
}