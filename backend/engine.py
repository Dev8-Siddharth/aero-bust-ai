"""
Core AI/ML Forecast Bust Detection and Confidence Estimation Engine.
Implements multi-factor non-linear error growth modeling, ensemble spread analysis,
and historical analog fingerprinting for medium-range forecasts (Day 1 to Day 10).
"""

import math
import numpy as np
from typing import Dict, List, Any, Optional
from .data.regions import get_all_regions, get_region_by_id
from .data.historical_busts import get_historical_busts

# Available Synoptic Weather Scenarios
WEATHER_SCENARIOS = {
    "monsoon_depression": {
        "id": "monsoon_depression",
        "name": "Active Monsoon Depression (Bay of Bengal to Central India)",
        "category": "Monsoon Dynamics",
        "description": "Deep depression over NW Bay of Bengal propagating WNW across Central India with intense monsoon surge.",
        "active_regions": ["central_india_monsoon", "bay_of_bengal_coast", "gangetic_plains_east", "west_coast_ghats"],
        "base_synoptics": {
            "vorticity_850": 21.4,
            "cape": 2100,
            "shear_200_850": 11.2,
            "z500_anomaly": -32.0,
            "pwat": 72.5,
            "ensemble_spread_norm": 0.78
        }
    },
    "tropical_cyclone": {
        "id": "tropical_cyclone",
        "name": "Very Severe Cyclonic Storm (East Coast / Bay of Bengal)",
        "category": "Tropical Cyclogenesis",
        "description": "Rapidly intensifying cyclone approaching Odisha/Andhra coast with high steering ridge divergence.",
        "active_regions": ["bay_of_bengal_coast", "gangetic_plains_east", "south_peninsular_interior"],
        "base_synoptics": {
            "vorticity_850": 26.5,
            "cape": 2700,
            "shear_200_850": 15.8,
            "z500_anomaly": 42.0,
            "pwat": 76.0,
            "ensemble_spread_norm": 0.85
        }
    },
    "western_disturbance": {
        "id": "western_disturbance",
        "name": "Severe Western Disturbance & Jet-Streak Overlap",
        "category": "Mid-Latitude Dynamics",
        "description": "Deep upper tropospheric trough with 130-knot subtropical jet streak impacting Western Himalayas & NW plains.",
        "active_regions": ["western_himalayas", "northwest_plains", "rajasthan_desert_arid"],
        "base_synoptics": {
            "vorticity_850": 12.8,
            "cape": 480,
            "shear_200_850": 36.5,
            "z500_anomaly": -68.0,
            "pwat": 30.5,
            "ensemble_spread_norm": 0.81
        }
    },
    "severe_heatwave": {
        "id": "severe_heatwave",
        "name": "Pre-Monsoon Extreme Heatwave & Anti-Cyclonic Dome",
        "category": "Thermodynamics & Radiation",
        "description": "Persistent 500hPa ridge with strong subsidence and depleted soil moisture feedback over NW & Central India.",
        "active_regions": ["rajasthan_desert_arid", "northwest_plains", "central_india_monsoon", "gujarat_saurashtra"],
        "base_synoptics": {
            "vorticity_850": -9.2,
            "cape": 350,
            "shear_200_850": 10.5,
            "z500_anomaly": 78.0,
            "pwat": 12.0,
            "ensemble_spread_norm": 0.62
        }
    },
    "break_monsoon": {
        "id": "break_monsoon",
        "name": "Break Monsoon Phase / Trough Shift to Foothills",
        "category": "Intraseasonal Oscillation",
        "description": "Sudden migration of monsoon trough axis to Himalayan foothills; suppression in Central India and deluge in NE.",
        "active_regions": ["northeast_india", "gangetic_plains_east", "central_india_monsoon"],
        "base_synoptics": {
            "vorticity_850": 14.5,
            "cape": 2350,
            "shear_200_850": 16.0,
            "z500_anomaly": 22.0,
            "pwat": 66.0,
            "ensemble_spread_norm": 0.83
        }
    }
}


class ForecastBustEngine:
    def __init__(self):
        self.regions = get_all_regions()
        self.historical_busts = get_historical_busts()

    def _cosine_similarity(self, v1: Dict[str, float], v2: Dict[str, float]) -> float:
        """Compute cosine similarity between two synoptic feature dictionaries."""
        keys = ["vorticity_850", "cape", "shear_200_850", "z500_anomaly", "pwat", "ensemble_spread_norm"]
        vec1 = np.array([float(v1.get(k, 0.0)) for k in keys])
        vec2 = np.array([float(v2.get(k, 0.0)) for k in keys])

        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.5
        sim = float(np.dot(vec1, vec2) / (norm1 * norm2))
        return max(0.0, min(1.0, (sim + 1.0) / 2.0))

    def find_historical_analogs(self, synoptics: Dict[str, float], top_k: int = 3) -> List[Dict[str, Any]]:
        """Identify closest historical NWP bust analogs matching current synoptic patterns."""
        analogs = []
        for bust in self.historical_busts:
            sim = self._cosine_similarity(synoptics, bust["synoptic_fingerprint"])
            analogs.append({
                "id": bust["id"],
                "name": bust["name"],
                "weather_system": bust["weather_system"],
                "lead_time_busted": bust["lead_time_busted"],
                "similarity_score": round(sim * 100, 1),
                "model_error_summary": bust["model_error_summary"],
                "historical_error_magnitude": bust["historical_error_magnitude"],
                "lesson_learned": bust["lesson_learned"]
            })
        analogs.sort(key=lambda x: x["similarity_score"], reverse=True)
        return analogs[:top_k]

    def compute_region_day_metrics(
        self,
        region: Dict[str, Any],
        scenario_key: str,
        lead_day: int,
        custom_params: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculates non-linear forecast confidence and bust probability for a specific region and lead day (1 to 10).
        """
        scenario = WEATHER_SCENARIOS.get(scenario_key, WEATHER_SCENARIOS["monsoon_depression"])
        syn = dict(scenario["base_synoptics"])
        if custom_params:
            syn.update(custom_params)

        is_active_region = region["id"] in scenario["active_regions"]

        # Climatological vulnerability multiplier
        clim_risk = region.get("climatological_bust_risk", "Moderate")
        clim_mult = 1.35 if clim_risk == "Severe" else (1.15 if clim_risk == "High" else 0.95)

        # Calibrated meteorological error growth curve
        lead_time_factor = (lead_day / 10.0) ** 1.15
        day_growth = math.exp(0.24 * (lead_day - 1)) - 1.0

        # Synoptic instability index [0 to 1]
        vort = abs(syn["vorticity_850"]) / 30.0
        cape = min(syn["cape"] / 3500.0, 1.0)
        shear = min(syn["shear_200_850"] / 40.0, 1.0)
        ens_spread = syn.get("ensemble_spread_norm", 0.7)
        instability_idx = 0.35 * vort + 0.35 * cape + 0.15 * shear + 0.15 * ens_spread

        # Active region factor
        region_exposure = 1.30 if is_active_region else 0.55

        # Normalized bust threat index [0.0 to 1.0]
        bust_index = (
            0.36 * lead_time_factor +
            0.28 * (ens_spread * region_exposure) +
            0.22 * (instability_idx * clim_mult * region_exposure) +
            0.14 * (day_growth * 0.12)
        )

        # Sigmoid centered around 0.44
        bust_prob = 1.0 / (1.0 + math.exp(-7.5 * (bust_index - 0.44)))
        bust_probability_pct = round(max(5.0, min(95.0, bust_prob * 100)), 1)

        # Confidence score: inverse of bust risk conditioned on lead time
        base_confidence = 100.0 - bust_probability_pct
        lead_penalty = (lead_day - 1) * 3.2
        confidence_pct = round(max(8.0, min(96.0, base_confidence * 0.92 - lead_penalty * 0.35)), 1)

        # Categorize Error-Prone Status
        if bust_probability_pct >= 70.0:
            status = "CRITICAL_BUST_RISK"
            status_label = "Critical Bust Risk"
            status_color = "#ef4444"
        elif bust_probability_pct >= 50.0:
            status = "HIGH_UNCERTAINTY"
            status_label = "High Uncertainty"
            status_color = "#f97316"
        elif bust_probability_pct >= 30.0:
            status = "MODERATE_UNCERTAINTY"
            status_label = "Moderate Uncertainty"
            status_color = "#eab308"
        else:
            status = "STABLE_FORECAST"
            status_label = "Reliable Forecast"
            status_color = "#10b981"

        # Estimated NWP Model Spread & Expected Error at this lead time
        ecmwf_spread = round(12.0 + (lead_day ** 1.6) * (3.8 * region_exposure), 1)
        gfs_spread = round(14.0 + (lead_day ** 1.65) * (4.2 * region_exposure), 1)
        ncum_spread = round(13.0 + (lead_day ** 1.62) * (4.0 * region_exposure), 1)

        return {
            "lead_day": lead_day,
            "confidence_pct": confidence_pct,
            "bust_probability_pct": bust_probability_pct,
            "status": status,
            "status_label": status_label,
            "status_color": status_color,
            "ensemble_spread_km": ecmwf_spread,
            "model_spreads": {
                "ECMWF_EPS": ecmwf_spread,
                "GEFS_GFS": gfs_spread,
                "IMD_NCUM": ncum_spread
            }
        }

    def analyze_forecast(
        self,
        scenario_key: str = "monsoon_depression",
        lead_day: int = 5,
        custom_params: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Executes full forecast bust detection across all regions for Day 1 to Day 10.
        """
        scenario = WEATHER_SCENARIOS.get(scenario_key, WEATHER_SCENARIOS["monsoon_depression"])
        syn = dict(scenario["base_synoptics"])
        if custom_params:
            syn.update(custom_params)

        regions_results = []
        critical_alert_zones = []
        overall_confidences = []
        overall_bust_probs = []

        for reg in self.regions:
            day_metrics = self.compute_region_day_metrics(reg, scenario_key, lead_day, custom_params)
            
            # Trajectory across Day 1 to Day 10
            trajectory = []
            for d in range(1, 11):
                m = self.compute_region_day_metrics(reg, scenario_key, d, custom_params)
                trajectory.append({
                    "day": d,
                    "confidence_pct": m["confidence_pct"],
                    "bust_probability_pct": m["bust_probability_pct"],
                    "ensemble_spread_km": m["ensemble_spread_km"]
                })

            reg_entry = {
                "id": reg["id"],
                "name": reg["name"],
                "zone": reg["zone"],
                "lat": reg["lat"],
                "lon": reg["lon"],
                "bounds": reg["bounds"],
                "climatological_bust_risk": reg["climatological_bust_risk"],
                "primary_bust_drivers": reg["primary_bust_drivers"],
                "current_day_metrics": day_metrics,
                "day_1_to_10_trajectory": trajectory
            }
            regions_results.append(reg_entry)

            overall_confidences.append(day_metrics["confidence_pct"])
            overall_bust_probs.append(day_metrics["bust_probability_pct"])

            if day_metrics["status"] in ["CRITICAL_BUST_RISK", "HIGH_UNCERTAINTY"]:
                critical_alert_zones.append({
                    "region_id": reg["id"],
                    "region_name": reg["name"],
                    "status": day_metrics["status"],
                    "status_label": day_metrics["status_label"],
                    "status_color": day_metrics["status_color"],
                    "bust_probability_pct": day_metrics["bust_probability_pct"],
                    "confidence_pct": day_metrics["confidence_pct"],
                    "primary_driver": reg["primary_bust_drivers"][0],
                    "all_drivers": reg["primary_bust_drivers"]
                })

        critical_alert_zones.sort(key=lambda x: x["bust_probability_pct"], reverse=True)
        analogs = self.find_historical_analogs(syn, top_k=3)

        subcontinent_trajectory = []
        for d in range(1, 11):
            day_conf_vals = [
                self.compute_region_day_metrics(r, scenario_key, d, custom_params)["confidence_pct"]
                for r in self.regions
            ]
            day_bust_vals = [
                self.compute_region_day_metrics(r, scenario_key, d, custom_params)["bust_probability_pct"]
                for r in self.regions
            ]
            subcontinent_trajectory.append({
                "day": d,
                "avg_confidence_pct": round(float(np.mean(day_conf_vals)), 1),
                "avg_bust_probability_pct": round(float(np.mean(day_bust_vals)), 1)
            })

        return {
            "scenario": scenario,
            "selected_lead_day": lead_day,
            "synoptic_parameters": syn,
            "national_summary": {
                "mean_confidence_pct": round(float(np.mean(overall_confidences)), 1),
                "mean_bust_probability_pct": round(float(np.mean(overall_bust_probs)), 1),
                "high_risk_zone_count": len([z for z in critical_alert_zones if z["status"] == "CRITICAL_BUST_RISK"]),
                "moderate_risk_zone_count": len([z for z in critical_alert_zones if z["status"] == "HIGH_UNCERTAINTY"]),
                "forecast_verdict": (
                    "EXTREME BUST DANGER: High divergence among multi-model ensembles. Forecasters advised to refrain from single-deterministic reliance."
                    if np.mean(overall_bust_probs) > 60 else
                    "ELEVATED UNCERTAINTY: Localized bust hotspots detected. Ensemble probabilistic envelope recommended."
                    if np.mean(overall_bust_probs) > 40 else
                    "FAVORABLE STABILITY: NWP solutions exhibit strong spatial-temporal agreement."
                )
            },
            "subcontinent_trajectory": subcontinent_trajectory,
            "critical_alert_zones": critical_alert_zones,
            "regions": regions_results,
            "top_historical_analogs": analogs
        }


engine = ForecastBustEngine()
