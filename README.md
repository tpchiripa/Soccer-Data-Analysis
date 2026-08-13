# FootballIQ

A full-stack football analytics and scouting platform. FootballIQ helps national federations track player performance for call-ups and helps clubs discover and compare transfer targets — combining a searchable player database, advanced scouting filters, a similarity engine, head-to-head comparisons, and a persistent watchlist, all behind real user authentication.

## Features

- **Player Search** — search FootballIQ's player database by name, with age, overall rating, and potential.
- **Scouting** — filter players by overall rating, potential, preferred foot, height, and weight to discover targets matching specific criteria.
- **Similarity Engine** — find players with statistically similar playing styles to any given player.
- **Comparison** — compare two players head-to-head, including their strongest differentiating attributes.
- **Watchlist** — save players you're tracking for call-ups or transfer targets, with notes and timestamps.
- **Authentication** — secure registration and login with hashed passwords and JWT-based sessions; all core features are protected behind login.
- **Dashboard** — an at-a-glance overview of database size, your watchlist count, and the current top-rated player.

## Machine Learning

Beyond the live application, the project includes an offline model-training pipeline (`train_model.py`) that clusters players into distinct archetypes using K-Means:

- **`FootballPipeline`** — runs the full data pipeline from raw SQLite tables through cleaning and feature engineering.
- **`FeatureEngineer`** — builds the numeric feature matrix used for clustering (skill ratings, physical attributes).
- **`PlayerClusterModel`** — trains a K-Means model (default 6 clusters) to group players into statistically distinct types — e.g. defenders, playmakers, finishers, goalkeepers — based on their attribute profiles rather than their listed position.
- **`ClusterAnalyzer`** — summarizes each cluster's defining characteristics and prints a full training report.

Run training with:
```bash
python train_model.py
```

This produces a saved, reusable clustering model and a printed report describing each player archetype discovered in the dataset. This clustering work originated from the project's initial data-analysis phase (see `notebooks/`) and has since been refactored into a reusable, testable pipeline.

## Tech Stack

**Backend**
- FastAPI (Python)
- SQLite (player data + user accounts + watchlist)
- Pandas, scikit-learn (K-Means clustering)
- JWT authentication (`python-jose`) with bcrypt password hashing (`passlib`)

**Frontend**
- React + TypeScript
- Vite
- Tailwind CSS
- React Router

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- The [European Soccer Database](https://www.kaggle.com/hugomathien/soccer) SQLite file, placed at `data/raw/database.sqlite`

### Backend Setup

```bash
# From the project root
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# Create a .env file in the project root with:
# JWT_SECRET=your_own_random_secret_string

uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

### Frontend Setup

```bash
cd footballiq-ui
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

## Project Structure

├── app/ # FastAPI application
│ ├── routers/ # API route handlers (players, scouting, similarity, comparison, watchlist, auth, dashboard)
│ ├── dependencies.py # Shared service instances
│ └── main.py # App entrypoint, middleware, router registration
├── src/
│ ├── data/ # Data loading, cleaning, and feature engineering
│ ├── models/ # Clustering model and cluster analysis
│ ├── pipeline.py # End-to-end data pipeline
│ └── services/ # Business logic (player, scouting, similarity, comparison, watchlist, auth)
├── footballiq-ui/ # React + TypeScript frontend
│ └── src/
│ ├── pages/ # Route-level views
│ ├── components/ # Reusable UI components
│ └── context/ # Auth context/state
├── notebooks/ # Original exploratory data analysis
├── train_model.py # Offline clustering model training script
└── data/raw/database.sqlite # Player dataset (not committed — see Data Source)
## Data Source

The current dataset is the [European Soccer Database](https://www.kaggle.com/hugomathien/soccer) from Kaggle, covering 11 European leagues from 2008–2016. It was used to get the platform's core features — and the clustering model — working end-to-end before investing in a paid, live data feed.

## Known Limitations & Roadmap

This is an actively evolving project. Current known gaps:

- **Dataset is historical, not live.** The European Soccer Database stops in 2016 and covers European leagues only — it does not include African leagues or current-season form.
- **No nationality or position fields** in the current dataset — these show as "N/A" in the UI.
- **Live data integration is planned.** [API-Football](https://www.api-football.com/) has been evaluated and confirmed to cover both European and African leagues (Nigeria's NPFL, Ghana's Premier League, South Africa's Premier Soccer League, Egypt's Premier League, and more) with real player identity, nationality, and position data. Full statistical data (goals, assists, minutes played) requires a paid plan, which is a planned upgrade once the platform has traction.
- **Single shared watchlist.** The watchlist is not yet scoped per-user — this is a natural next step now that authentication is in place.

## Disclaimer

This project is under active development as a personal portfolio and learning project, demonstrating full-stack development, data engineering, machine learning, and product design for a real-world use case in football scouting and analytics.