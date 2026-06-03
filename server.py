"""
HU Voice AI - Combined Web Server
Serves both frontend (static files) and backend API on the same port
"""

import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from api.main import app as api_app

# Create combined app
app = FastAPI(title="HU Voice AI - Combined Server")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount API under /api prefix to avoid route conflicts
app.mount("/api", api_app)

# Serve index.html for root and SPA routes
@app.get("/")
async def root():
    return FileResponse("templates/index.html", media_type="text/html")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Skip if it's a known API or static path
    if full_path.startswith("api/") or full_path.startswith("static/"):
        return {"error": "Not found"}
    
    file_path = os.path.join("templates", full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Default to index.html for SPA routing
    return FileResponse("templates/index.html", media_type="text/html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n{'='*60}")
    print(f"🚀 HU Voice AI - Combined Server")
    print(f"{'='*60}")
    print(f"📱 Access on this device: http://localhost:{port}")
    print(f"📱 Access on other device: http://[YOUR_IP]:{port}")
    print(f"📱 Get your IP: ipconfig (Windows) or ifconfig (Mac/Linux)")
    print(f"{'='*60}\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
