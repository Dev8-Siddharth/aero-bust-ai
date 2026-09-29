"""
Meteorological Sub-divisions and Regions for India / South Asia.
Includes coordinates, climatological vulnerability factors, and typical NWP bust triggers.
"""

REGIONS_DATA = [
    {
        "id": "west_coast_ghats",
        "name": "Konkan, Goa & Western Ghats",
        "zone": "Peninsular West",
        "lat": 16.5,
        "lon": 73.8,
        "bounds": [[13.5, 72.5], [19.5, 75.0]],
        "climatological_bust_risk": "High",
        "primary_bust_drivers": [
            "Steep orographic rainfall triggering",
            "Offshore trough oscillation",
            "Meso-scale cloud burst under-resolution in 12km NWP grids"
        ],
        "historical_mean_mae_d5": 42.4
    },
    {
        "id": "central_india_monsoon",
        "name": "Central India (MP, Vidarbha & Chhattisgarh)",
        "zone": "Central",
        "lat": 22.5,
        "lon": 79.5,
        "bounds": [[19.0, 75.5], [25.0, 83.5]],
        "climatological_bust_risk": "Severe",
        "primary_bust_drivers": [
            "Monsoon depression track deviation",
            "Vorticity shear zone displacement",
            "Soil moisture-convection feedback coupling"
        ],
        "historical_mean_mae_d5": 38.1
    },
    {
        "id": "western_himalayas",
        "name": "Western Himalayas (J&K, HP, Uttarakhand)",
        "zone": "North",
        "lat": 32.5,
        "lon": 76.5,
        "bounds": [[29.5, 73.5], [35.5, 80.5]],
        "climatological_bust_risk": "Severe",
        "primary_bust_drivers": [
            "Subtropical westerly jet streak interaction",
            "Freezing-level / snow-line transition altitude error",
            "Valley-ridge micro-circulations unresolved by global NWP"
        ],
        "historical_mean_mae_d5": 34.6
    },
    {
        "id": "northwest_plains",
        "name": "Northwest Plains (Punjab, Haryana, Delhi, W. UP)",
        "zone": "North-West",
        "lat": 29.0,
        "lon": 76.8,
        "bounds": [[27.0, 74.0], [31.5, 79.0]],
        "climatological_bust_risk": "Moderate",
        "primary_bust_drivers": [
            "Western disturbance induced cyclonic circulation (WD-ICC)",
            "Pre-monsoon squall lines / dust storms (Andhi)",
            "Boundary layer inversion and fog burn-off timing"
        ],
        "historical_mean_mae_d5": 22.3
    },
    {
        "id": "bay_of_bengal_coast",
        "name": "Odisha & North Coastal Andhra",
        "zone": "East Coast",
        "lat": 19.8,
        "lon": 85.0,
        "bounds": [[16.5, 82.0], [22.0, 87.5]],
        "climatological_bust_risk": "Severe",
        "primary_bust_drivers": [
            "Tropical cyclogenesis rapid intensification (RI)",
            "Landfall azimuth timing errors (cross-track vs along-track)",
            "Coastal frontogenesis and surge precipitation enhancement"
        ],
        "historical_mean_mae_d5": 48.7
    },
    {
        "id": "gangetic_plains_east",
        "name": "Gangetic West Bengal & Bihar",
        "zone": "East",
        "lat": 24.5,
        "lon": 86.5,
        "bounds": [[22.0, 84.0], [27.0, 89.0]],
        "climatological_bust_risk": "High",
        "primary_bust_drivers": [
            "Nor'wester (Kalbaishakhi) severe thunderstorm genesis",
            "Monsoon trough oscillation northward toward foothills",
            "Mid-tropospheric moisture convergence pulse"
        ],
        "historical_mean_mae_d5": 31.9
    },
    {
        "id": "northeast_india",
        "name": "North-East India (Assam, Meghalaya & Hills)",
        "zone": "North-East",
        "lat": 26.0,
        "lon": 92.5,
        "bounds": [[23.5, 89.5], [28.5, 96.0]],
        "climatological_bust_risk": "High",
        "primary_bust_drivers": [
            "Funneling orographic flow in Brahmaputra valley",
            "Monsoon break phase localized hyper-rainfall (Cherrapunji effect)",
            "Bay of Bengal moisture tap surge"
        ],
        "historical_mean_mae_d5": 45.2
    },
    {
        "id": "rajasthan_desert_arid",
        "name": "West & East Rajasthan",
        "zone": "Arid North-West",
        "lat": 26.5,
        "lon": 72.5,
        "bounds": [[24.0, 69.5], [29.5, 76.5]],
        "climatological_bust_risk": "Moderate",
        "primary_bust_drivers": [
            "Sensible heat flux & boundary layer super-heating",
            "Dry-line moisture intrusion boundary errors",
            "Extreme heatwave temperature persistence vs cold pool advection"
        ],
        "historical_mean_mae_d5": 19.5
    },
    {
        "id": "gujarat_saurashtra",
        "name": "Gujarat, Saurashtra & Kutch",
        "zone": "West",
        "lat": 22.8,
        "lon": 71.0,
        "bounds": [[20.5, 68.5], [24.5, 73.5]],
        "climatological_bust_risk": "High",
        "primary_bust_drivers": [
            "Arabian Sea cyclone recurvature vs Oman track divergence",
            "Mid-tropospheric cyclone (MTC) quasi-stationary stalling",
            "Vigorous monsoon surge interaction"
        ],
        "historical_mean_mae_d5": 36.8
    },
    {
        "id": "south_peninsular_interior",
        "name": "South Interior Karnataka, Rayalaseema & TN",
        "zone": "South",
        "lat": 13.5,
        "lon": 77.5,
        "bounds": [[10.5, 75.5], [16.0, 80.5]],
        "climatological_bust_risk": "Moderate",
        "primary_bust_drivers": [
            "Northeast monsoon easterly wave timing",
            "Rain-shadow lee-wave convection triggering",
            "Inter-tropical convergence zone (ITCZ) migration pulses"
        ],
        "historical_mean_mae_d5": 25.4
    }
]

def get_all_regions():
    return REGIONS_DATA

def get_region_by_id(region_id: str):
    for r in REGIONS_DATA:
        if r["id"] == region_id:
            return r
    return None
