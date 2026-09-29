/**
 * AERO-BUST AI : Client Application Logic
 * Integrates Leaflet geospatial mapping, Chart.js multi-lead predictability decay,
 * Training Datasets Catalog, and AI meteorological explainability.
 */

const state = {
  currentScenario: "monsoon_depression",
  currentLeadDay: 5,
  currentLayer: "bust",
  currentTab: "forecast", // 'forecast' | 'datasets'
  customParams: null,
  analysisData: null,
  datasetsData: null,
  selectedRegionId: null,
  map: null,
  mapLayers: null,
  decayChart: null,
  modelsChart: null,
  isExplaining: false
};

document.addEventListener("DOMContentLoaded", async () => {
  initIcons();
  initTabs();
  initDayPills();
  initMap();
  initCharts();
  bindEvents();
  await loadForecastAnalysis();
  await loadDatasets();
  await triggerAIExplain();
});

function initIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

function initTabs() {
  const btnForecast = document.getElementById("btn-tab-forecast");
  const btnDatasets = document.getElementById("btn-tab-datasets");
  const btnBack = document.getElementById("btn-back-to-forecast");

  btnForecast.addEventListener("click", () => switchTab("forecast"));
  btnDatasets.addEventListener("click", () => switchTab("datasets"));
  if (btnBack) {
    btnBack.addEventListener("click", () => switchTab("forecast"));
  }
}

function switchTab(tab) {
  state.currentTab = tab;
  const viewForecast = document.getElementById("view-forecast");
  const viewDatasets = document.getElementById("view-datasets");
  const controlsBar = document.getElementById("forecast-controls-bar");
  const btnForecast = document.getElementById("btn-tab-forecast");
  const btnDatasets = document.getElementById("btn-tab-datasets");

  if (tab === "forecast") {
    viewForecast.classList.remove("hidden");
    viewDatasets.classList.add("hidden");
    controlsBar.classList.remove("hidden");

    btnForecast.className = "px-3 py-1.5 bg-cyan-600 text-white text-xs font-semibold rounded-lg shadow-sm flex items-center gap-1.5 transition";
    btnDatasets.className = "px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-emerald-300 text-xs font-semibold rounded-lg border border-emerald-800/60 flex items-center gap-1.5 transition";

    if (state.map) {
      setTimeout(() => state.map.invalidateSize(), 150);
    }
  } else {
    viewForecast.classList.add("hidden");
    viewDatasets.classList.remove("hidden");
    controlsBar.classList.add("hidden");

    btnForecast.className = "px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-lg border border-slate-700 flex items-center gap-1.5 transition";
    btnDatasets.className = "px-3 py-1.5 bg-emerald-600 text-white text-xs font-semibold rounded-lg shadow-sm flex items-center gap-1.5 transition";
  }
}

function initDayPills() {
  const container = document.getElementById("day-pills-container");
  container.innerHTML = "";
  for (let d = 1; d <= 10; d++) {
    const btn = document.createElement("button");
    btn.className = `day-pill px-2.5 py-1 text-xs font-semibold rounded-md border border-slate-700 bg-slate-800 text-slate-300 hover:text-white ${
      d === state.currentLeadDay ? "active" : ""
    }`;
    btn.dataset.day = d;
    btn.innerHTML = `D${d} <span class="text-[10px] opacity-75 font-normal">(${d * 24}h)</span>`;
    btn.addEventListener("click", () => {
      setLeadDay(d);
    });
    container.appendChild(btn);
  }
}

function setLeadDay(day) {
  state.currentLeadDay = day;
  document.querySelectorAll(".day-pill").forEach((el) => {
    if (parseInt(el.dataset.day) === day) {
      el.classList.add("active");
    } else {
      el.classList.remove("active");
    }
  });
  document.getElementById("lead-day-display").textContent = `Lead Time: Day ${day} (${day * 24} Hours)`;
  loadForecastAnalysis();
}

function initMap() {
  state.map = L.map("weather-map", {
    zoomControl: true,
    attributionControl: false
  }).setView([22.5, 80.0], 5);

  L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
    maxZoom: 16,
    subdomains: ["server", "services"]
  }).addTo(state.map);

  state.mapLayers = L.layerGroup().addTo(state.map);
}

function initCharts() {
  const ctxDecay = document.getElementById("chart-decay").getContext("2d");
  state.decayChart = new Chart(ctxDecay, {
    type: "line",
    data: {
      labels: ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"],
      datasets: [
        {
          label: "Forecast Confidence (%)",
          data: [],
          borderColor: "#10b981",
          backgroundColor: "rgba(16, 185, 129, 0.15)",
          borderWidth: 2,
          tension: 0.35,
          fill: true
        },
        {
          label: "Bust Probability (%)",
          data: [],
          borderColor: "#ef4444",
          backgroundColor: "rgba(239, 68, 68, 0.15)",
          borderWidth: 2,
          tension: 0.35,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { labels: { color: "#94a3b8", font: { size: 10 } } },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          titleColor: "#38bdf8",
          bodyColor: "#f8fafc"
        }
      },
      scales: {
        x: { grid: { color: "rgba(255,255,255,0.05)" }, ticks: { color: "#94a3b8", font: { size: 10 } } },
        y: {
          min: 0,
          max: 100,
          grid: { color: "rgba(255,255,255,0.05)" },
          ticks: { color: "#94a3b8", font: { size: 10 }, callback: (v) => v + "%" }
        }
      }
    }
  });

  const ctxModels = document.getElementById("chart-models").getContext("2d");
  state.modelsChart = new Chart(ctxModels, {
    type: "line",
    data: {
      labels: ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"],
      datasets: [
        {
          label: "ECMWF EPS (km)",
          data: [],
          borderColor: "#38bdf8",
          borderWidth: 2,
          tension: 0.3
        },
        {
          label: "GEFS / GFS (km)",
          data: [],
          borderColor: "#f97316",
          borderWidth: 2,
          tension: 0.3
        },
        {
          label: "IMD NCUM (km)",
          data: [],
          borderColor: "#a855f7",
          borderWidth: 2,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#94a3b8", font: { size: 10 } } },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          titleColor: "#38bdf8",
          bodyColor: "#f8fafc"
        }
      },
      scales: {
        x: { grid: { color: "rgba(255,255,255,0.05)" }, ticks: { color: "#94a3b8", font: { size: 10 } } },
        y: {
          grid: { color: "rgba(255,255,255,0.05)" },
          ticks: { color: "#94a3b8", font: { size: 10 }, callback: (v) => v + "km" }
        }
      }
    }
  });
}

function bindEvents() {
  document.getElementById("scenario-select").addEventListener("change", (e) => {
    state.currentScenario = e.target.value;
    state.selectedRegionId = null;
    hideInspector();
    loadForecastAnalysis();
    triggerAIExplain();
  });

  document.getElementById("btn-layer-bust").addEventListener("click", () => setMapLayer("bust"));
  document.getElementById("btn-layer-conf").addEventListener("click", () => setMapLayer("conf"));
  document.getElementById("btn-layer-spread").addEventListener("click", () => setMapLayer("spread"));

  document.getElementById("btn-explain-ai").addEventListener("click", () => {
    triggerAIExplain();
  });

  document.getElementById("btn-export-bulletin").addEventListener("click", exportForecasterBulletin);
  document.getElementById("btn-close-inspector").addEventListener("click", hideInspector);

  const sandboxModal = document.getElementById("sandbox-modal");
  document.getElementById("btn-sandbox-toggle").addEventListener("click", () => {
    sandboxModal.classList.remove("hidden");
  });
  document.getElementById("btn-close-sandbox").addEventListener("click", () => {
    sandboxModal.classList.add("hidden");
  });

  bindSliderPreview("input-vort", "val-vort", " x 10^-5 s^-1");
  bindSliderPreview("input-cape", "val-cape", " J/kg");
  bindSliderPreview("input-shear", "val-shear", " m/s");
  bindSliderPreview("input-pwat", "val-pwat", " mm");
  bindSliderPreview("input-spread", "val-spread", "");

  document.getElementById("btn-apply-sandbox").addEventListener("click", () => {
    state.customParams = {
      vorticity_850: parseFloat(document.getElementById("input-vort").value),
      cape: parseFloat(document.getElementById("input-cape").value),
      shear_200_850: parseFloat(document.getElementById("input-shear").value),
      pwat: parseFloat(document.getElementById("input-pwat").value),
      ensemble_spread_norm: parseFloat(document.getElementById("input-spread").value)
    };
    sandboxModal.classList.add("hidden");
    loadForecastAnalysis();
    triggerAIExplain();
  });

  document.getElementById("btn-reset-sandbox").addEventListener("click", () => {
    state.customParams = null;
    sandboxModal.classList.add("hidden");
    loadForecastAnalysis();
    triggerAIExplain();
  });
}

function bindSliderPreview(inputId, displayId, suffix) {
  const input = document.getElementById(inputId);
  const display = document.getElementById(displayId);
  input.addEventListener("input", (e) => {
    display.textContent = e.target.value + suffix;
  });
}

function setMapLayer(layer) {
  state.currentLayer = layer;
  ["bust", "conf", "spread"].forEach((l) => {
    const btn = document.getElementById(`btn-layer-${l}`);
    if (l === layer) {
      btn.className = "px-2.5 py-1 rounded-md bg-cyan-600 text-white font-medium transition";
    } else {
      btn.className = "px-2.5 py-1 rounded-md text-slate-300 hover:text-white transition";
    }
  });
  renderMapLayers();
}

async function loadForecastAnalysis() {
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        scenario_key: state.currentScenario,
        lead_day: state.currentLeadDay,
        custom_params: state.customParams
      })
    });

    if (!response.ok) throw new Error("Failed to fetch forecast analysis");
    state.analysisData = await response.json();

    updateKPIs();
    renderMapLayers();
    renderAlerts();
    renderAnalogs();
    updateCharts();
    if (state.selectedRegionId) {
      updateInspector();
    }
  } catch (err) {
    console.error("Error analyzing forecast:", err);
  }
}

async function loadDatasets() {
  try {
    const res = await fetch("/api/datasets");
    if (!res.ok) throw new Error("Failed to load datasets metadata");
    state.datasetsData = await res.json();
    renderDatasetsView();
  } catch (err) {
    console.error("Error loading datasets:", err);
  }
}

function renderDatasetsView() {
  const container = document.getElementById("datasets-cards-container");
  if (!container || !state.datasetsData) return;

  const datasets = state.datasetsData.datasets || [];
  container.innerHTML = "";

  datasets.forEach((ds) => {
    const card = document.createElement("div");
    card.className = "glass-panel p-4 flex flex-col justify-between border border-slate-800 hover:border-emerald-500/50 transition";
    
    const paramsList = ds.parameters.map((p) => `<li class="truncate">${p}</li>`).join("");

    card.innerHTML = `
      <div>
        <div class="flex items-center justify-between gap-2">
          <span class="text-xs font-bold text-emerald-400 uppercase tracking-wide">${ds.id.replace('_', ' ')}</span>
          <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">${ds.data_volume}</span>
        </div>
        <h4 class="text-sm font-bold text-slate-100 mt-1">${ds.name}</h4>
        <p class="text-[11px] text-slate-400 mt-0.5"><strong>Source:</strong> ${ds.source}</p>
        <div class="mt-2 text-[11px] text-slate-300 bg-slate-800/50 p-2 rounded border border-slate-700/60">
          <div><span class="text-slate-400">Coverage:</span> ${ds.period}</div>
          <div><span class="text-slate-400">Resolution:</span> ${ds.resolution}</div>
        </div>
        <div class="mt-2.5">
          <span class="text-[10px] uppercase font-semibold text-slate-400 block mb-1">Key Meteorological Parameters:</span>
          <ul class="text-[11px] text-slate-300 list-disc list-inside space-y-0.5">
            ${paramsList}
          </ul>
        </div>
      </div>
      <div class="mt-3 pt-2.5 border-t border-slate-800 text-[11px] text-emerald-300/90 leading-snug">
        <strong>Role in Model Training:</strong> ${ds.training_role}
      </div>
    `;
    container.appendChild(card);
  });
}

function updateKPIs() {
  const data = state.analysisData;
  if (!data) return;

  const summary = data.national_summary;

  const confVal = document.getElementById("kpi-confidence-val");
  const confBar = document.getElementById("kpi-confidence-bar");
  const confBadge = document.getElementById("kpi-confidence-badge");
  confVal.textContent = `${summary.mean_confidence_pct}%`;
  confBar.style.width = `${summary.mean_confidence_pct}%`;

  if (summary.mean_confidence_pct >= 60) {
    confBadge.textContent = "High Skill";
    confBadge.className = "text-xs font-medium px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800";
    confVal.className = "text-3xl font-extrabold text-emerald-400";
    confBar.className = "bg-emerald-500 h-1.5 rounded-full transition-all duration-500";
  } else if (summary.mean_confidence_pct >= 40) {
    confBadge.textContent = "Moderate Skill";
    confBadge.className = "text-xs font-medium px-2 py-0.5 rounded-full bg-yellow-950 text-yellow-300 border border-yellow-800";
    confVal.className = "text-3xl font-extrabold text-yellow-400";
    confBar.className = "bg-yellow-500 h-1.5 rounded-full transition-all duration-500";
  } else {
    confBadge.textContent = "Low Skill";
    confBadge.className = "text-xs font-medium px-2 py-0.5 rounded-full bg-rose-950 text-rose-300 border border-rose-800";
    confVal.className = "text-3xl font-extrabold text-rose-400";
    confBar.className = "bg-rose-500 h-1.5 rounded-full transition-all duration-500";
  }

  const bustVal = document.getElementById("kpi-bust-val");
  const bustBar = document.getElementById("kpi-bust-bar");
  const bustBadge = document.getElementById("kpi-bust-badge");
  bustVal.textContent = `${summary.mean_bust_probability_pct}%`;
  bustBar.style.width = `${summary.mean_bust_probability_pct}%`;

  if (summary.mean_bust_probability_pct >= 65) {
    bustBadge.textContent = "Severe Bust Threat";
    bustBadge.className = "text-xs font-medium px-2 py-0.5 rounded-full bg-rose-950 text-rose-300 border border-rose-800 pulse-critical";
  } else if (summary.mean_bust_probability_pct >= 40) {
    bustBadge.textContent = "Elevated Bust Threat";
    bustBadge.className = "text-xs font-medium px-2 py-0.5 rounded-full bg-orange-950 text-orange-300 border border-orange-800";
  } else {
    bustBadge.textContent = "Low Bust Threat";
    bustBadge.className = "text-xs font-medium px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800";
  }

  const totalHotspots = summary.high_risk_zone_count + summary.moderate_risk_zone_count;
  document.getElementById("kpi-hotspots-val").textContent = totalHotspots;
  document.getElementById("kpi-hotspots-sub").textContent = `${summary.high_risk_zone_count} Critical, ${summary.moderate_risk_zone_count} High Uncertainty`;

  const analogs = data.top_historical_analogs;
  if (analogs && analogs.length > 0) {
    const top = analogs[0];
    document.getElementById("kpi-analog-name").textContent = top.name;
    document.getElementById("kpi-analog-sim").textContent = `${top.similarity_score}% Match`;
    document.getElementById("kpi-analog-desc").textContent = top.model_error_summary;
  }

  document.getElementById("verdict-text").textContent = summary.forecast_verdict;
}

function renderMapLayers() {
  if (!state.mapLayers || !state.analysisData) return;
  state.mapLayers.clearLayers();

  state.analysisData.regions.forEach((reg) => {
    const metrics = reg.current_day_metrics;
    let color = "#10b981";
    let fillOpacity = 0.45;
    let radius = 45000;

    if (state.currentLayer === "bust") {
      color = metrics.status_color;
      fillOpacity = Math.max(0.35, metrics.bust_probability_pct / 120);
      radius = 35000 + (metrics.bust_probability_pct * 800);
    } else if (state.currentLayer === "conf") {
      color = metrics.confidence_pct > 60 ? "#10b981" : metrics.confidence_pct > 35 ? "#eab308" : "#ef4444";
      fillOpacity = Math.max(0.3, metrics.confidence_pct / 120);
      radius = 35000 + (metrics.confidence_pct * 700);
    } else if (state.currentLayer === "spread") {
      color = metrics.ensemble_spread_km > 50 ? "#a855f7" : metrics.ensemble_spread_km > 30 ? "#38bdf8" : "#22c55e";
      fillOpacity = 0.5;
      radius = 30000 + (metrics.ensemble_spread_km * 900);
    }

    const polygon = L.polygon(reg.bounds, {
      color: color,
      weight: state.selectedRegionId === reg.id ? 3 : 1.5,
      fillColor: color,
      fillOpacity: fillOpacity * 0.4,
      dashArray: state.selectedRegionId === reg.id ? "4, 4" : null
    });

    const circle = L.circle([reg.lat, reg.lon], {
      color: color,
      weight: 2,
      fillColor: color,
      fillOpacity: fillOpacity,
      radius: radius
    });

    const tooltipContent = `
      <div class="p-1 font-sans">
        <div class="font-bold text-cyan-300 text-xs">${reg.name}</div>
        <div class="text-[11px] text-slate-300 mt-1">
          Bust Prob: <span class="font-bold text-rose-400">${metrics.bust_probability_pct}%</span> | 
          Conf: <span class="font-bold text-emerald-400">${metrics.confidence_pct}%</span>
        </div>
        <div class="text-[10px] text-slate-400">Spread: ${metrics.ensemble_spread_km} km | Status: ${metrics.status_label}</div>
      </div>
    `;
    circle.bindTooltip(tooltipContent, { className: "custom-leaflet-tooltip", sticky: true });
    polygon.bindTooltip(tooltipContent, { className: "custom-leaflet-tooltip", sticky: true });

    const onClick = () => {
      selectRegion(reg.id);
    };
    circle.on("click", onClick);
    polygon.on("click", onClick);

    state.mapLayers.addLayer(polygon);
    state.mapLayers.addLayer(circle);
  });
}

function selectRegion(regionId) {
  state.selectedRegionId = regionId;
  renderMapLayers();
  updateInspector();
  triggerAIExplain(regionId);
}

function updateInspector() {
  if (!state.selectedRegionId || !state.analysisData) return;
  const reg = state.analysisData.regions.find((r) => r.id === state.selectedRegionId);
  if (!reg) return;

  const card = document.getElementById("region-inspector-card");
  card.classList.remove("hidden");

  document.getElementById("inspector-name").textContent = reg.name;
  const badge = document.getElementById("inspector-badge");
  badge.textContent = reg.current_day_metrics.status_label;
  badge.style.backgroundColor = reg.current_day_metrics.status_color + "22";
  badge.style.color = reg.current_day_metrics.status_color;
  badge.style.borderColor = reg.current_day_metrics.status_color + "66";

  document.getElementById("inspector-bust").textContent = `${reg.current_day_metrics.bust_probability_pct}%`;
  document.getElementById("inspector-conf").textContent = `${reg.current_day_metrics.confidence_pct}%`;
  document.getElementById("inspector-spread").textContent = `${reg.current_day_metrics.ensemble_spread_km} km`;
  document.getElementById("inspector-clim").textContent = reg.climatological_bust_risk;

  const driversList = document.getElementById("inspector-drivers");
  driversList.innerHTML = "";
  reg.primary_bust_drivers.forEach((drv) => {
    const li = document.createElement("li");
    li.textContent = drv;
    driversList.appendChild(li);
  });
}

function hideInspector() {
  state.selectedRegionId = null;
  document.getElementById("region-inspector-card").classList.add("hidden");
  renderMapLayers();
}

function renderAlerts() {
  const container = document.getElementById("alerts-list");
  const badge = document.getElementById("alerts-count-badge");
  const alerts = state.analysisData.critical_alert_zones;

  badge.textContent = `${alerts.length} Zones`;
  container.innerHTML = "";

  if (alerts.length === 0) {
    container.innerHTML = `
      <div class="p-3 text-center text-xs text-slate-400 bg-slate-800/40 rounded-lg">
        No critical forecast bust zones detected at Lead Day ${state.currentLeadDay}.
      </div>
    `;
    return;
  }

  alerts.forEach((alt) => {
    const item = document.createElement("div");
    item.className = `p-2.5 rounded-lg border transition cursor-pointer flex flex-col gap-1.5 ${
      state.selectedRegionId === alt.region_id
        ? "bg-slate-800 border-cyan-500 shadow-md shadow-cyan-500/10"
        : "bg-slate-800/50 hover:bg-slate-800 border-slate-700/70"
    }`;
    item.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold text-slate-200">${alt.region_name}</span>
        <span class="text-[11px] font-bold px-2 py-0.5 rounded-full" style="background-color: ${alt.status_color}22; color: ${alt.status_color}; border: 1px solid ${alt.status_color}55">
          ${alt.status_label}
        </span>
      </div>
      <div class="flex items-center justify-between text-xs text-slate-400">
        <span>Bust Risk: <strong class="text-rose-400">${alt.bust_probability_pct}%</strong></span>
        <span>Confidence: <strong class="text-emerald-400">${alt.confidence_pct}%</strong></span>
      </div>
      <p class="text-[11px] text-slate-400 flex items-center gap-1 line-clamp-1">
        <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span> ${alt.primary_driver}
      </p>
    `;
    item.addEventListener("click", () => {
      selectRegion(alt.region_id);
    });
    container.appendChild(item);
  });
}

function renderAnalogs() {
  const container = document.getElementById("analogs-list");
  const analogs = state.analysisData.top_historical_analogs;
  container.innerHTML = "";

  if (!analogs || analogs.length === 0) {
    container.innerHTML = `<div class="text-xs text-slate-400 p-2">No analogs matched.</div>`;
    return;
  }

  analogs.forEach((ana) => {
    const div = document.createElement("div");
    div.className = "p-2.5 bg-slate-800/50 rounded-lg border border-slate-700/60 text-xs";
    div.innerHTML = `
      <div class="flex items-center justify-between font-semibold text-slate-200">
        <span class="truncate max-w-[220px]">${ana.name}</span>
        <span class="text-cyan-400 font-bold bg-cyan-950 px-1.5 py-0.5 rounded border border-cyan-800 text-[11px]">
          ${ana.similarity_score}% Match
        </span>
      </div>
      <div class="text-[11px] text-slate-400 mt-1">
        <span class="text-amber-400 font-medium">Bust Window:</span> ${ana.lead_time_busted}
      </div>
      <p class="text-[11px] text-slate-300 mt-1 line-clamp-2">
        <span class="text-slate-400">Error Mode:</span> ${ana.model_error_summary}
      </p>
      <div class="mt-1.5 pt-1.5 border-t border-slate-700/50 text-[11px] text-emerald-300">
        <strong>Lesson:</strong> ${ana.lesson_learned}
      </div>
    `;
    container.appendChild(div);
  });
}

function updateCharts() {
  if (!state.analysisData) return;

  const trajectory = state.analysisData.subcontinent_trajectory;
  const confData = trajectory.map((t) => t.avg_confidence_pct);
  const bustData = trajectory.map((t) => t.avg_bust_probability_pct);

  state.decayChart.data.datasets[0].data = confData;
  state.decayChart.data.datasets[1].data = bustData;
  state.decayChart.update();

  const ecmwf = [];
  const gfs = [];
  const ncum = [];
  for (let d = 1; d <= 10; d++) {
    ecmwf.push(round1(12.0 + Math.pow(d, 1.6) * 4.2));
    gfs.push(round1(14.0 + Math.pow(d, 1.65) * 4.6));
    ncum.push(round1(13.0 + Math.pow(d, 1.62) * 4.4));
  }
  state.modelsChart.data.datasets[0].data = ecmwf;
  state.modelsChart.data.datasets[1].data = gfs;
  state.modelsChart.data.datasets[2].data = ncum;
  state.modelsChart.update();
}

function round1(val) {
  return Math.round(val * 10) / 10;
}

async function triggerAIExplain(regionId = null) {
  if (state.isExplaining) return;
  state.isExplaining = true;

  const loading = document.getElementById("ai-loading");
  const content = document.getElementById("ai-content");
  const sourceBadge = document.getElementById("ai-engine-source");

  loading.classList.remove("hidden");
  content.innerHTML = "";

  try {
    const res = await fetch("/api/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        scenario_key: state.currentScenario,
        lead_day: state.currentLeadDay,
        target_region_id: regionId,
        custom_params: state.customParams
      })
    });

    if (!res.ok) throw new Error("Explanation API failed");
    const data = await res.json();

    sourceBadge.textContent = data.source || "AI Engine";

    if (window.marked) {
      content.innerHTML = window.marked.parse(data.explanation_markdown || "No explanation provided.");
    } else {
      content.textContent = data.explanation_markdown;
    }
  } catch (err) {
    console.error("AI Explain error:", err);
    content.innerHTML = `<p class="text-rose-400">Failed to generate AI diagnostic explanation. Please retry.</p>`;
  } finally {
    loading.classList.add("hidden");
    state.isExplaining = false;
  }
}

function exportForecasterBulletin() {
  const summary = state.analysisData?.national_summary || {};
  const scenario = state.analysisData?.scenario || {};
  const leadDay = state.currentLeadDay;
  const aiText = document.getElementById("ai-content").innerHTML;

  const printWindow = window.open("", "_blank");
  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>IMD/NCMRWF NWP Forecast Bust Advisory - Day ${leadDay}</title>
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 30px; color: #111; line-height: 1.5; }
        h1 { color: #0284c7; border-bottom: 2px solid #0284c7; padding-bottom: 8px; }
        .meta-box { background: #f1f5f9; padding: 15px; border-radius: 6px; margin-bottom: 20px; font-size: 14px; }
        .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-weight: bold; background: #fee2e2; color: #991b1b; }
        .prose h3 { color: #0369a1; margin-top: 18px; }
        .footer { margin-top: 40px; font-size: 11px; color: #64748b; border-top: 1px solid #cbd5e1; padding-top: 10px; }
      </style>
    </head>
    <body>
      <h1>OFFICIAL OPERATIONAL FORECAST BUST ADVISORY</h1>
      <div class="meta-box">
        <strong>Weather Regime:</strong> ${scenario.name || "Synoptic Pattern"}<br>
        <strong>Lead Time Horizon:</strong> Day ${leadDay} (${leadDay * 24} Hours)<br>
        <strong>Subcontinent Mean Bust Threat:</strong> <span class="badge">${summary.mean_bust_probability_pct}%</span><br>
        <strong>Mean Forecast Confidence:</strong> ${summary.mean_confidence_pct}%<br>
        <strong>Critical Hotspot Zones:</strong> ${summary.high_risk_zone_count} regions identified
      </div>
      <div class="prose">
        ${aiText}
      </div>
      <div class="footer">
        Generated by AERO-BUST AI Platform for India Meteorological Department (IMD) & National Centre for Medium Range Weather Forecasting (NCMRWF).
      </div>
      <script>window.print();</script>
    </body>
    </html>
  `);
  printWindow.document.close();
}
