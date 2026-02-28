"""FastAPI application entry-point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.database import init_db

_FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup tasks (DB init) then yield to the application."""
    init_db()
    yield


app = FastAPI(
    title="Brezhoneg Validation",
    description="Plateforme de validation collaborative du corpus parallèle breton–français",
    version="0.1.0",
    lifespan=lifespan,
)

# -- CORS (dev) ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -- API routes ----------------------------------------------------------------
@app.get("/api/hello")
async def hello():
    """Sanity-check endpoint — returns a greeting in Breton."""
    return {"message": "Demat Bed"}


# -- Serve Vue frontend (production) ------------------------------------------
if _FRONTEND_DIST.is_dir():
    app.mount("/assets", StaticFiles(directory=_FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve static files or fall back to index.html for SPA routing."""
        file = (_FRONTEND_DIST / full_path).resolve()
        if file.is_file() and str(file).startswith(str(_FRONTEND_DIST.resolve())):
            return FileResponse(file)
        return FileResponse(_FRONTEND_DIST / "index.html")
