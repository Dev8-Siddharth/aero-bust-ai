"""
Launch script for AI-Based Forecast Bust Detection Prototype.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Forecast Bust Detection Server on http://127.0.0.1:{port}")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=port, reload=False)
