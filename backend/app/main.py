"""
Main entry point for the Cyber Hub backend.
This is where FastAPI starts, tables are created, and all routes are registered.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.api.routes.users import router as users_router
from app.api.routes.research import router as research_router
from app.api.routes.hub import router as hub_router

# Import models so SQLAlchemy knows about them when creating tables
from app.models import user, research, agent, agent_request 




@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup — creates all DB tables if they don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")
    yield
    print("👋 Shutting down Cyber Hub")


app = FastAPI(
    title="Cyber Hub API",
    description="Multi-agent simulation platform — Agent Hub + Research Area",
    version="0.1.0",
    lifespan=lifespan
)

# Allow React frontend (running on port 3000) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route groups
app.include_router(users_router)
app.include_router(research_router)
app.include_router(hub_router)


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to Cyber Hub 🤖",
        "areas": ["Agent Hub", "Research Area"],
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
