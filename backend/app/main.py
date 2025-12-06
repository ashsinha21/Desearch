from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.routers import search, metrics
from app.services.db import init_db
from app.services.meili_client import init_meilisearch

app = FastAPI(title="DESearch API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    # Initialize database
    await init_db()
    # Initialize MeiliSearch
    await init_meilisearch()

# Include routers
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(metrics.router, prefix="/api", tags=["metrics"])

@app.get("/")
async def root():
    return {"message": "DESearch API is running"}
