"""
Global configuration for Trading Tools application
Centralized file paths and settings
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
EXPORTS_DIR = BASE_DIR / "data"

# MT4 export file path
MT4_EXPORT_FILE = EXPORTS_DIR / "trade_data.htm"

# Templates directory
TEMPLATES_DIR = BASE_DIR / "src" / "templates"

# Static files directory
STATIC_DIR = BASE_DIR / "src" / "static"
STATIC_CSS_DIR = STATIC_DIR / "css"
STATIC_JS_DIR = STATIC_DIR / "js"
STATIC_CHARTS_DIR = STATIC_DIR / "charts"

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[CONFIG] Base directory: {BASE_DIR}")
    print(f"[CONFIG] MT4 export file: {MT4_EXPORT_FILE}")
    print(f"[CONFIG] Templates directory: {TEMPLATES_DIR}")
    print(f"[CONFIG] Static directory: {STATIC_DIR}")

# Application settings
DEBUG = False
HOST = "127.0.0.1"
PORT = 8000

# Chart settings
CHART_WIDTH = 1200
CHART_HEIGHT = 400

# File upload settings (for future file upload functionality)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.htm', '.html'}
