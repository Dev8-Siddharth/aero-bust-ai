"""
Catalog of benchmark Historical NWP Forecast Busts in South Asia.
Used for analog pattern matching, error climatology attribution, and model comparison.
"""

HISTORICAL_BUSTS_CATALOG = [
    {
        "id": "bust_2023_biparjoy",
        "name": "Cyclone Biparjoy Track Recurvature Bust (June 2023)",
        "weather_system": "Tropical Cyclone",
        "affected_regions": ["gujarat_saurashtra", "rajasthan_desert_arid"],
        "nwp_failure_type": "Recurvature & Steering Ridge Ambiguity",
        "lead_time_busted": "Day 4 - Day 7 (96h - 168h)",
        "observed_phenomenon": "Extremely Severe Cyclonic Storm (ESCS) stalled and took sharp north-east recurvature toward Kutch/Jakhau Port.",
        "model_error_summary": "Global ECMWF and GFS ensemble members were initially split into two bimodal branches: one toward Oman/Pakistan, one toward Gujarat. Deterministic runs shifted landfall by >420 km within 48h cycles.",
        "historical_error_magnitude": "Track error >380 km; Rainfall over Saurashtra underpredicted by 210 mm/day.",
        "synoptic_fingerprint": {
            "vorticity_850": 18.5,
            "cape": 2400,
            "shear_200_850": 14.2,
            "z500_anomaly": 48.0,
            "pwat": 68.0,
            "ensemble_spread_norm": 0.88
        },
        "lesson_learned": "Ensemble bimodality in sub-tropical ridge position is a primary indicator of Day 5+ track busts."
    },
    {
        "id": "bust_2022_central_depression",
        "name": "Central India Deep Depression Track Stalling Bust (August 2022)",
        "weather_system": "Monsoon Depression",
        "affected_regions": ["central_india_monsoon", "gangetic_plains_east", "gujarat_saurashtra"],
        "nwp_failure_type": "Slow Propagation & Extreme Precipitation Underestimation",
        "lead_time_busted": "Day 3 - Day 6 (72h - 144h)",
        "observed_phenomenon": "Monsoon depression over Bay of Bengal moved across Odisha and stalled over Madhya Pradesh & East Rajasthan, causing historic flooding.",
        "model_error_summary": "NWP models forecasted fast westward progression into Pakistan within 48 hours. The system became quasi-stationary due to mid-latitude trough coupling, dumping 350% normal rainfall.",
        "historical_error_magnitude": "Precipitation volume underforecasted by 185 mm over 48h; Track speed overpredicted by 14 km/h.",
        "synoptic_fingerprint": {
            "vorticity_850": 22.0,
            "cape": 1850,
            "shear_200_850": 9.5,
            "z500_anomaly": -38.0,
            "pwat": 74.0,
            "ensemble_spread_norm": 0.79
        },
        "lesson_learned": "High PWAT coupled with slow 500hPa steering flow leads to catastrophic heavy precipitation forecast failure."
    },
    {
        "id": "bust_2021_western_disturbance",
        "name": "Intense Western Disturbance & Jet-Streak Overlap (Feb 2021)",
        "weather_system": "Western Disturbance",
        "affected_regions": ["western_himalayas", "northwest_plains"],
        "nwp_failure_type": "Orographic Freezing-Level & Snowfall Boundary Bust",
        "lead_time_busted": "Day 4 - Day 8 (96h - 192h)",
        "observed_phenomenon": "Upper tropospheric trough interacted with Arabian Sea moisture flux, producing rapid cryogenic flash flood and extreme snowfall in upper catchment.",
        "model_error_summary": "NWP predicted a shallow passing trough with light drizzle. Instead, mid-tropospheric jet streak intensified rapidly, triggering heavy snow-melt and flash flooding.",
        "historical_error_magnitude": "Snow/liquid water equivalent missed by 65mm; Snowline altitude underestimated by 700m.",
        "synoptic_fingerprint": {
            "vorticity_850": 11.2,
            "cape": 450,
            "shear_200_850": 34.0,
            "z500_anomaly": -65.0,
            "pwat": 28.0,
            "ensemble_spread_norm": 0.82
        },
        "lesson_learned": "Strong 200hPa jet core (>50 m/s) over Western Himalayas amplifies non-linear error growth exponentially past Day 3."
    },
    {
        "id": "bust_2022_march_heatwave",
        "name": "Premature Early Heatwave & Land-Atmosphere Feedback (March 2022)",
        "weather_system": "Heatwave",
        "affected_regions": ["rajasthan_desert_arid", "northwest_plains", "central_india_monsoon"],
        "nwp_failure_type": "Extreme Maximum Temperature (Tmax) Underforecast",
        "lead_time_busted": "Day 5 - Day 10 (120h - 240h)",
        "observed_phenomenon": "Hottest March in 122 years across NW and Central India with persistent anti-cyclonic subsidence.",
        "model_error_summary": "Models continuously forecasted relief and western disturbance intrusion at Days 5-7. The anti-cyclonic heat dome persisted due to depleted soil moisture feedback.",
        "historical_error_magnitude": "Tmax underestimated by 4.5?C to 6.2?C consistently at Day 5+ lead times.",
        "synoptic_fingerprint": {
            "vorticity_850": -8.5,
            "cape": 320,
            "shear_200_850": 12.0,
            "z500_anomaly": 72.0,
            "pwat": 14.0,
            "ensemble_spread_norm": 0.65
        },
        "lesson_learned": "Soil moisture memory and persistent 500hPa geopotential ridges cause systematic cold bias in NWP medium-range heat forecasts."
    },
    {
        "id": "bust_2023_ghats_orographic",
        "name": "Western Ghats Coastal Cloudburst / Offshore Trough Bust (July 2023)",
        "weather_system": "Heavy Rainfall / Orographic",
        "affected_regions": ["west_coast_ghats", "south_peninsular_interior"],
        "nwp_failure_type": "Sub-Grid Orographic Convective Triggering",
        "lead_time_busted": "Day 2 - Day 5 (48h - 120h)",
        "observed_phenomenon": "Torrential continuous downpours (>400 mm/24h in Raigad/Ratnagiri) triggered by an offshore trough embedded in strong southwesterlies.",
        "model_error_summary": "Coarse 12-25 km NWP grid resolved only smooth coastal rain (50-80mm), failing to capture the meso-vortex trapped against the Western Ghats escarpment.",
        "historical_error_magnitude": "24-hour rainfall underestimated by 320 mm; False negative for red alert at Day 4.",
        "synoptic_fingerprint": {
            "vorticity_850": 15.8,
            "cape": 2200,
            "shear_200_850": 18.0,
            "z500_anomaly": -12.0,
            "pwat": 72.0,
            "ensemble_spread_norm": 0.74
        },
        "lesson_learned": "Offshore trough with 850hPa winds perpendicular to Ghats (>35 knots) has 82% bust probability in quantitative precipitation forecasts (QPF)."
    },
    {
        "id": "bust_2024_break_monsoon",
        "name": "Active-to-Break Monsoon Transition & Foothill Shift (July 2024)",
        "weather_system": "Break/Active Monsoon Phase",
        "affected_regions": ["northeast_india", "central_india_monsoon", "gangetic_plains_east"],
        "nwp_failure_type": "Monsoon Trough Axis Latitude Dislocation",
        "lead_time_busted": "Day 4 - Day 8 (96h - 192h)",
        "observed_phenomenon": "Abrupt shift of monsoon trough to Himalayan foothills, shutting off rain in central India while unleashing devastating floods in Assam/Bihar.",
        "model_error_summary": "NWP models delayed the break onset by 4 days, predicting continuing central Indian rainfall while underestimating northeast extreme totals.",
        "historical_error_magnitude": "Spatial precipitation pattern inverted (R=-0.38 correlation with truth at Day 5).",
        "synoptic_fingerprint": {
            "vorticity_850": 14.0,
            "cape": 2100,
            "shear_200_850": 15.0,
            "z500_anomaly": 25.0,
            "pwat": 65.0,
            "ensemble_spread_norm": 0.81
        },
        "lesson_learned": "Madden-Julian Oscillation (MJO) phase transitions into Indian Ocean suppressors create rapid monsoon trough break dislocations."
    }
]

def get_historical_busts():
    return HISTORICAL_BUSTS_CATALOG
