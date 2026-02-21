from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, projects, search, analysis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code here runs on startup
    print(f"🚀 {settings.app_name} starting in {settings.app_env} mode")
    yield
    # Code here runs on shutdown
    print("👋 Shutting down")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered academic project discovery platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allows your Flutter app (on a different port/domain) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.app_name}