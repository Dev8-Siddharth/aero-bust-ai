"""
FastAPI Server for AI-Based Forecast Bust Detection.
Serves REST APIs for analysis, analog matching, AI explainability, training datasets, and UI.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, Optional

from .engine import engine, WEATHER_SCENARIOS
from .ai_service import AIMeteorologicalExplainer
from .data.regions import get_all_regions
from .data.historical_busts import get_historical_busts
from .data.datasets import get_training_datasets, get_model_metrics

app = FastAPI(
    title="AI-Based Forecast Bust Detection System",
    description="Operational Medium-Range NWP Uncertainty & Forecast Bust Detection for India & South Asia",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

explainer = AIMeteorologicalExplainer()

class AnalyzeRequest(BaseModel):
    scenario_key: str = "monsoon_depression"
    lead_day: int = 5
    custom_params: Optional[Dict[str, float]] = None

class ExplainRequest(BaseModel):
    scenario_key: str = "monsoon_depression"
    lead_day: int = 5
    target_region_id: Optional[str] = None
    custom_params: Optional[Dict[str, float]] = None

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "NWP Forecast Bust Detection AI Engine"}

@app.get("/api/scenarios")
def get_scenarios():
    return {"scenarios": WEATHER_SCENARIOS}

@app.get("/api/regions")
def get_regions():
    return {"regions": get_all_regions()}

@app.get("/api/historical-busts")
def get_busts():
    return {"historical_busts": get_historical_busts()}

@app.get("/api/datasets")
def get_datasets():
    return {
        "datasets": get_training_datasets(),
        "model_metrics": get_model_metrics()
    }

@app.post("/api/analyze")
def analyze_forecast(req: AnalyzeRequest):
    if req.lead_day < 1 or req.lead_day > 10:
        raise HTTPException(status_code=400, detail="lead_day must be between 1 and 10")
    
    result = engine.analyze_forecast(
        scenario_key=req.scenario_key,
        lead_day=req.lead_day,
        custom_params=req.custom_params
    )
    return result

@app.post("/api/explain")
def explain_forecast(req: ExplainRequest):
    analysis_data = engine.analyze_forecast(
        scenario_key=req.scenario_key,
        lead_day=req.lead_day,
        custom_params=req.custom_params
    )
    explanation = explainer.explain_forecast_bust(
        analysis_data=analysis_data,
        target_region_id=req.target_region_id
    )
    return explanation

# Mount static frontend
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
