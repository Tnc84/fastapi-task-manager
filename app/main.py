"""
FastAPI Task Manager Application
Main application entry point
"""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A modern task management API built with FastAPI",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# CORS middleware - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router FIRST - this is critical for route precedence
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Serve Angular static files (must be after API routes to avoid conflicts)
# Support both local frontend folder and external Angular project
frontend_paths = [
    Path(__file__).parent.parent / "frontend" / "dist" / "browser",
    Path(__file__).parent.parent / "frontend" / "dist",
    Path("D:/Angular/task-manager-portal/dist/task-manager-portal/browser"),
    Path("D:/Angular/task-manager-portal/dist/task-manager-portal"),
    Path("D:/Angular/task-manager-portal/dist/browser"),
    Path("D:/Angular/task-manager-portal/dist"),
]

frontend_dist = None
for path in frontend_paths:
    if path.exists():
        frontend_dist = path
        break

if frontend_dist is not None:
    # Root route - serve Angular index.html
    @app.get("/", include_in_schema=False)
    async def serve_angular_root():
        """Serve Angular app at root"""
        return FileResponse(frontend_dist / "index.html")
    
    # Catch-all route for Angular static files and SPA routing
    # This MUST be after all API routes to avoid conflicts
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_angular_spa(full_path: str, request: Request):
        """
        Serve Angular SPA static files and handle client-side routing
        Returns the requested file if it exists, otherwise returns index.html for Angular routing
        Explicitly excludes API routes to prevent conflicts
        """
        # Explicitly skip API paths - let FastAPI's router handle them
        # This prevents the catch-all from intercepting API requests
        if full_path.startswith("api/") or full_path.startswith("health"):
            # This should never be reached if routes are registered properly
            # But acts as a safety net
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")
        
        # Construct the file path
        file_path = frontend_dist / full_path
        
        # If the file exists, serve it (JS, CSS, images, etc.)
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Otherwise, return index.html for Angular's client-side routing
        return FileResponse(frontend_dist / "index.html")
else:
    # No frontend available, show API message
    @app.get("/")
    async def root():
        """Root endpoint - shown when no frontend is available"""
        return {"message": "Welcome to Task Manager API", "docs": f"{settings.API_V1_STR}/docs"}
