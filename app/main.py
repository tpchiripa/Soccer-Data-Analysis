"""
FootballIQ API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.players import router as players_router
from app.routers.profile import router as profile_router
from app.routers.similarity import router as similarity_router
from app.routers.comparison import router as comparison_router
from app.routers.scouting import router as scouting_router
from app.routers.dashboard import router as dashboard_router

app = FastAPI(
    title="FootballIQ API",
    description="Football Analytics Platform powered by Machine Learning",
    version="1.0.0",
)

# Allow the Vite dev server to call this API.
# Add your deployed frontend's URL here too once you have one.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(players_router)
app.include_router(profile_router)
app.include_router(similarity_router)
app.include_router(comparison_router)
app.include_router(scouting_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "application": "FootballIQ",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }