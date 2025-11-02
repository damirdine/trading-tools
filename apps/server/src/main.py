from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api.routes import router, api_router
from config import TEMPLATES_DIR, STATIC_DIR
import os

app = FastAPI(title="Trading Tools API", version="0.1.0")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Mount static files
static_dir = str(STATIC_DIR)
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(router)
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "trading-tools-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)