import * as maplibregl from "https://unpkg.com/maplibre-gl@6.11.2/dist/maplibre-gl.mjs";

// Upper bounds (in days) and colors for binning image age, defined by the legend markup so
// it renders before any data loads.
const AGE_BINS = [...document.querySelectorAll("#legend-items li")].map((li) => ({
  max: Number(li.dataset.max),
  color: li.style.getPropertyValue("--color").trim(),
  countEl: li.querySelector(".count"),
}));

// Datasets available to display, written by each dataset on update. Each entry links a CSV
// of the latest image timestamp per collection (seconds since the Unix epoch, 0 if no
// images) to a GeoJSON grid that shares its index columns.
const SCHEMA_URL = new URL("data/datasets.json", location);
// Loaded on demand to test which cells intersect an uploaded area of interest.
const TURF_URL = "https://cdn.jsdelivr.net/npm/@turf/boolean-intersects@7.2.0/+esm";
const SOURCE = "grid";
const AOI_SOURCE = "aoi";
const DAY = 86400;
const now = Date.now() / 1000;

const datasetSelect = document.getElementById("dataset");
const collectionSelect = document.getElementById("collection");
const statusEl = document.getElementById("status");
const minDateInput = document.getElementById("min-date");
const minDateClear = document.getElementById("min-date-clear");
const filtersEl = document.getElementById("filters");
const filtersActive = document.getElementById("filters-active");
const aoiFile = document.getElementById("aoi-file");
const aoiName = document.getElementById("aoi-name");
const aoiClear = document.getElementById("aoi-clear");
const aoiError = document.getElementById("aoi-error");
const summaryCount = document.getElementById("summary-count");
const summaryLatency = document.getElementById("summary-latency");
const summaryOldest = document.getElementById("summary-oldest");
const summaryNewest = document.getElementById("summary-newest");

// Lucide icon paths (https://lucide.dev) shown alongside the status text.
const ICONS = {
  clock: '<path d="M12 6v6l4 2"/><circle cx="12" cy="12" r="10"/>',
  "triangle-alert":
    '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/>' +
    '<path d="M12 9v4"/><path d="M12 17h.01"/>',
};
const panel = document.getElementById("panel");
const panelToggle = document.getElementById("panel-toggle");
const panelBody = document.getElementById("panel-body");
const panelTitle = document.getElementById("panel-title");

// Collapsible panel on narrow displays. The toggle is hidden on wide displays, so expand
// the panel when crossing over to keep its contents reachable.
function setPanelExpanded(expanded) {
  panel.classList.toggle("collapsed", !expanded);
  panelToggle.setAttribute("aria-expanded", expanded);
  panelBody.inert = !expanded;
}

panelToggle.addEventListener("click", () => {
  setPanelExpanded(panelToggle.getAttribute("aria-expanded") !== "true");
});
matchMedia("(max-width: 600px)").addEventListener("change", (e) => {
  if (!e.matches) setPanelExpanded(true);
});

const cache = {};
const gridCache = {};

const DATASETS = await fetchJson(SCHEMA_URL).catch((err) => {
  showError(err);
  throw err;
});

const params = new URLSearchParams(location.search);
let datasetId = DATASETS[params.get("dataset")] ? params.get("dataset") : Object.keys(DATASETS)[0];
let collection = DATASETS[datasetId].collections.includes(params.get("collection"))
  ? params.get("collection")
  : DATASETS[datasetId].collections[0];
// Earliest acquisition time to show, in seconds since the Unix epoch (0 to show all).
let minTime = 0;
// Uploaded area of interest, with the keys of intersecting cells cached by grid (null if none).
let aoi = null;
let booleanIntersects;
// The selected dataset as displayed, limited to the area of interest.
let shown = null;

setMinDate(params.get("after"));
minDateInput.max = new Date().toISOString().slice(0, 10);
filtersEl.open = minTime > 0;

const map = new maplibregl.Map({
  container: "map",
  // style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
  // style: "https://tiles.versatiles.org/assets/styles/colorful/style.json",
  style: "https://tiles.openfreemap.org/styles/fiord",
  // style: {
  //   version: 8,
  //   sources: {
  //     "raster-tiles": {
  //       type: "raster",
  //       tiles: ["https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2025_3857/default/g/{z}/{y}/{x}.jpg"],
  //       tileSize: 256,
  //       attribution: "<a href=\"https://cloudless.eox.at\">EOxCloudless</a> by EOX IT Services GmbH (Contains modified Copernicus Sentinel data 2025)",
  //     },
  //   },
  //   layers: [{ id: "raster-layer", type: "raster", source: "raster-tiles" }],
  // },
  center: [0, 20],
  zoom: 1.5,
  hash: "map",
});
map.addControl(new maplibregl.NavigationControl(), "top-right");

function formatDate(seconds) {
  return new Date(seconds * 1000).toISOString().slice(0, 19).replace("T", " ");
}

// Parse a `YYYY-MM-DD` date as UTC midnight in seconds, or 0 if missing or invalid.
function parseDate(value) {
  const ms = /^\d{4}-\d{2}-\d{2}$/.test(value ?? "") ? Date.parse(`${value}T00:00:00Z`) : NaN;
  return Number.isNaN(ms) ? 0 : ms / 1000;
}

function ageDays(seconds) {
  return (now - seconds) / DAY;
}

const relativeFormat = new Intl.RelativeTimeFormat("en", { numeric: "auto" });
const TIME_UNITS = [
  ["day", DAY],
  ["hour", 3600],
  ["minute", 60],
  ["second", 1],
];

// Humanize the offset from now, e.g. "3 hours ago".
function timeAgo(seconds) {
  const delta = seconds - now;
  const [unit, size] = TIME_UNITS.find(([, size]) => Math.abs(delta) >= size) ?? ["second", 1];
  return relativeFormat.format(Math.round(delta / size), unit);
}

// Style expression that bins the selected collection's timestamp into age colors.
function fillColor() {
  const age = ["/", ["-", now, ["get", collection]], DAY];
  const expr = ["step", age, AGE_BINS[0].color];
  AGE_BINS.slice(0, -1).forEach((bin, i) => expr.push(bin.max, AGE_BINS[i + 1].color));
  return expr;
}

// Show cells with images acquired on or after the minimum date.
const isVisible = () => [
  "all",
  [">", ["get", collection], 0],
  [">=", ["get", collection], minTime],
];
const isVisibleTime = (t) => t > 0 && t >= minTime;

function populateSelect(select, options, selected) {
  select.replaceChildren(
    ...options.map(([value, label]) => new Option(label, value, false, value === selected))
  );
  select.classList.remove("skeleton");
  select.disabled = false;
}

// Show skeletons in place of the status and legend counts while a dataset loads.
function setStatus(icon, text) {
  if (!text) return statusEl.replaceChildren();
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "icon");
  svg.setAttribute("viewBox", "0 0 24 24");
  svg.setAttribute("width", "14");
  svg.setAttribute("height", "14");
  svg.setAttribute("aria-hidden", "true");
  svg.innerHTML = ICONS[icon];
  statusEl.replaceChildren(svg, text);
}

function setLoading(loading) {
  const summaryEls = [summaryCount, summaryLatency, summaryOldest, summaryNewest];
  for (const el of [statusEl, ...summaryEls, ...AGE_BINS.map((bin) => bin.countEl)]) {
    el.classList.toggle("skeleton", loading);
  }
}

function updateUrl() {
  const url = new URL(location);
  url.searchParams.set("dataset", datasetId);
  url.searchParams.set("collection", collection);
  if (minTime) url.searchParams.set("after", minDateInput.value);
  else url.searchParams.delete("after");
  history.replaceState(null, "", url);
}

function median(values) {
  const sorted = values.toSorted((a, b) => a - b);
  const mid = sorted.length >> 1;
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function setSummaryDate(el, seconds) {
  el.textContent = seconds ? formatDate(seconds).slice(0, 10) : "–";
  el.title = seconds ? `${formatDate(seconds)} UTC` : "";
}

// Summarize the latest images of visible cells. Latency is the time from acquisition to the
// dataset's last update.
function updateSummary({ geojson, updated }) {
  const valid = geojson.features.map((f) => f.properties[collection]).filter(isVisibleTime);
  const latest = valid.length ? Math.max(...valid) : 0;
  const oldest = valid.length ? Math.min(...valid) : 0;
  const latency = valid.length && updated ? median(valid.map((t) => updated - t)) : null;

  summaryCount.textContent = valid.length.toLocaleString();
  summaryLatency.textContent = latency === null ? "–" : `${(latency / DAY).toFixed(1)} days`;
  setSummaryDate(summaryOldest, oldest);
  setSummaryDate(summaryNewest, latest);

  const counts = AGE_BINS.map(() => 0);
  for (const t of valid) {
    counts[AGE_BINS.findIndex((bin) => ageDays(t) < bin.max)]++;
  }

  AGE_BINS.forEach((bin, i) => (bin.countEl.textContent = counts[i].toLocaleString()));
}

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`);
  return res.json();
}

// Grids are shared between datasets, so cache them separately by URL.
function loadGrid(url) {
  gridCache[url] ??= fetchJson(url);
  return gridCache[url];
}

const UPDATE_HEADER = "# updated:";

// Parse a CSV of timestamps by index, with an optional `# updated: <seconds>` first line.
function parseTimestamps(text, index) {
  const lines = text.trim().split("\n");
  const updated = lines[0].startsWith(UPDATE_HEADER)
    ? Number(lines.shift().slice(UPDATE_HEADER.length))
    : null;
  const header = lines.shift().split(",");
  const timeCols = header.filter((col) => !index.includes(col));
  const rows = new Map();
  for (const line of lines) {
    const props = Object.fromEntries(line.split(",").map((value, i) => [header[i], value]));
    rows.set(
      indexKey(index, props),
      Object.fromEntries(timeCols.map((col) => [col, Number(props[col])]))
    );
  }
  return { rows, updated };
}

const indexKey = (index, props) => index.map((col) => String(props[col])).join("|");

// Load a dataset by joining its timestamps onto its grid, dropping cells without images
// in any collection, and record when it was last updated. Prefer the update time stored
// in the file, falling back to when the file was last modified.
async function loadDataset(id) {
  if (!cache[id]) {
    const { data, grid, index, collections } = DATASETS[id];
    const dataUrl = new URL(data, SCHEMA_URL);
    const [res, gridGeojson] = await Promise.all([
      fetch(dataUrl),
      loadGrid(new URL(grid, SCHEMA_URL)),
    ]);
    if (!res.ok) throw new Error(`Failed to load ${dataUrl}: ${res.status}`);
    const { rows, updated } = parseTimestamps(await res.text(), index);

    const features = [];
    for (const f of gridGeojson.features) {
      const row = rows.get(indexKey(index, f.properties));
      if (row && collections.some((c) => row[c] > 0)) {
        features.push({ ...f, properties: { ...f.properties, ...row } });
      }
    }
    const modified = Date.parse(res.headers.get("Last-Modified")) / 1000;
    cache[id] = {
      geojson: { type: "FeatureCollection", features },
      updated: updated || modified || null,
    };
  }
  return cache[id];
}

// Fill `{COLUMN}` placeholders in a dataset's label template from feature properties.
function featureLabel(template, props) {
  return template.replace(/\{(\w+)\}/g, (_, col) => props[col]);
}

async function selectDataset(id) {
  datasetId = id;
  const { collections } = DATASETS[id];
  if (!collections.includes(collection)) collection = collections[0];
  populateSelect(collectionSelect, collections.map((c) => [c, c]), collection);
  return showDataset();
}

// Incremented per load, so a slow load doesn't replace a newer selection.
let loadCount = 0;

async function showDataset() {
  const count = ++loadCount;
  setLoading(true);
  const loaded = await loadDataset(datasetId);
  const keys = aoi && (await intersectingKeys(datasetId));
  if (count !== loadCount) return;

  // Cells outside the area of interest are dropped rather than filtered, so they're excluded
  // from the summary too.
  const { index } = DATASETS[datasetId];
  const features = keys
    ? loaded.geojson.features.filter((f) => keys.has(indexKey(index, f.properties)))
    : loaded.geojson.features;
  shown = { ...loaded, geojson: { type: "FeatureCollection", features } };
  map.getSource(SOURCE).setData(shown.geojson);
  setStatus("clock", loaded.updated ? `Updated ${timeAgo(loaded.updated)}` : "");
  selectCollection(collection);
  setLoading(false);
}

function selectCollection(c) {
  collection = c;
  map.setPaintProperty("cells-fill", "fill-color", fillColor());
  applyFilter();
  panelTitle.textContent = c;
  panelTitle.classList.remove("skeleton");
}

function applyFilter() {
  map.setFilter("cells-fill", isVisible());
  map.setFilter("cells-line", isVisible());
  if (shown) updateSummary(shown);
  updateUrl();
}

function setMinDate(value) {
  minTime = parseDate(value);
  minDateInput.value = minTime ? value : "";
  minDateClear.hidden = !minTime;
  updateFiltersActive();
}

function updateFiltersActive() {
  filtersActive.hidden = !minTime && !aoi;
}

// Bounding box of nested coordinate arrays as [west, south, east, north].
function coordBounds(coords, bounds = [Infinity, Infinity, -Infinity, -Infinity]) {
  if (typeof coords[0] === "number") {
    bounds[0] = Math.min(bounds[0], coords[0]);
    bounds[1] = Math.min(bounds[1], coords[1]);
    bounds[2] = Math.max(bounds[2], coords[0]);
    bounds[3] = Math.max(bounds[3], coords[1]);
  } else {
    for (const c of coords) coordBounds(c, bounds);
  }
  return bounds;
}

const boundsIntersect = (a, b) => a[0] <= b[2] && b[0] <= a[2] && a[1] <= b[3] && b[1] <= a[3];

// Flatten a GeoJSON object of any type into its non-empty, non-collection geometries.
function geometries(geojson) {
  switch (geojson?.type) {
    case "FeatureCollection":
      return (geojson.features ?? []).flatMap(geometries);
    case "Feature":
      return geometries(geojson.geometry);
    case "GeometryCollection":
      return (geojson.geometries ?? []).flatMap(geometries);
    case "Point":
    case "MultiPoint":
    case "LineString":
    case "MultiLineString":
    case "Polygon":
    case "MultiPolygon":
      return geojson.coordinates?.length ? [geojson] : [];
    default:
      return [];
  }
}

// Keys of a dataset's grid cells that intersect the area of interest, computed once per grid
// using bounding boxes to skip exact tests on distant cells.
function intersectingKeys(id) {
  const { grid, index } = DATASETS[id];
  aoi.keys[grid] ??= loadGrid(new URL(grid, SCHEMA_URL)).then((gridGeojson) => {
    const keys = new Set();
    for (const f of gridGeojson.features) {
      const bounds = coordBounds(f.geometry.coordinates);
      const hit = aoi.parts.some(
        (part) => boundsIntersect(bounds, part.bounds) && booleanIntersects(f.geometry, part.geometry)
      );
      if (hit) keys.add(indexKey(index, f.properties));
    }
    return keys;
  });
  return aoi.keys[grid];
}

async function setAoi(file) {
  // Allow re-selecting the same file after it's edited or failed to load.
  aoiFile.value = "";
  aoiError.hidden = true;
  try {
    const parts = geometries(JSON.parse(await file.text())).map((geometry) => ({
      geometry,
      bounds: coordBounds(geometry.coordinates),
    }));
    if (!parts.length) throw new Error("No geometries found in file.");
    booleanIntersects ??= (await import(TURF_URL)).booleanIntersects;
    aoi = { name: file.name, parts, keys: {} };
  } catch (err) {
    console.error(err);
    aoiError.textContent = err instanceof SyntaxError ? "File is not valid JSON." : err.message;
    aoiError.hidden = false;
    return;
  }

  const geojson = {
    type: "FeatureCollection",
    features: aoi.parts.map(({ geometry }) => ({ type: "Feature", properties: {}, geometry })),
  };
  map.getSource(AOI_SOURCE).setData(geojson);
  zoomToAoi();
  showAoiState();
  await showDataset();
}

function clearAoi() {
  aoi = null;
  aoiError.hidden = true;
  map.getSource(AOI_SOURCE).setData({ type: "FeatureCollection", features: [] });
  showAoiState();
  return showDataset();
}

function showAoiState() {
  aoiName.textContent = aoi?.name ?? "Choose file";
  aoiClear.hidden = !aoi;
  updateFiltersActive();
}

// Fit the area of interest in the part of the map left uncovered by the panel.
function zoomToAoi() {
  const [west, south, east, north] = aoi.parts.reduce(
    (b, part) => [
      Math.min(b[0], part.bounds[0]),
      Math.min(b[1], part.bounds[1]),
      Math.max(b[2], part.bounds[2]),
      Math.max(b[3], part.bounds[3]),
    ],
    [Infinity, Infinity, -Infinity, -Infinity]
  );
  const padding = matchMedia("(max-width: 600px)").matches
    ? { top: 48, right: 48, bottom: panel.offsetHeight + 24, left: 48 }
    : { top: 48, right: 72, bottom: 48, left: panel.offsetLeft + panel.offsetWidth + 48 };
  map.fitBounds([west, south, east, north], { padding, maxZoom: 10 });
}

map.on("style.load", () => {
  map.setProjection({ type: "globe" });
});

map.on("load", async () => {
  map.addSource(SOURCE, {
    type: "geojson",
    data: { type: "FeatureCollection", features: [] },
    generateId: true,
  });

  map.addLayer({
    id: "cells-fill",
    type: "fill",
    source: SOURCE,
    paint: {
      "fill-color": fillColor(),
      "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false], 0.9, 0.4],
    },
  });
  map.addLayer({
    id: "cells-line",
    type: "line",
    source: SOURCE,
    paint: {
      "line-color": "#ffffff",
      "line-opacity": ["interpolate", ["linear"], ["zoom"], 2, 0.03, 6, 0.3],
      "line-width": 0.5,
    },
  });

  map.addSource(AOI_SOURCE, {
    type: "geojson",
    data: { type: "FeatureCollection", features: [] },
  });
  // Dark casing under a light outline, so the area reads over any cell color.
  map.addLayer({
    id: "aoi-casing",
    type: "line",
    source: AOI_SOURCE,
    paint: { "line-color": "#16181d", "line-width": 4, "line-opacity": 0.8 },
  });
  map.addLayer({
    id: "aoi-line",
    type: "line",
    source: AOI_SOURCE,
    paint: { "line-color": "#ffffff", "line-width": 2 },
  });
  map.addLayer({
    id: "aoi-point",
    type: "circle",
    source: AOI_SOURCE,
    filter: ["==", ["geometry-type"], "Point"],
    paint: {
      "circle-radius": 4,
      "circle-color": "#ffffff",
      "circle-stroke-color": "#16181d",
      "circle-stroke-width": 2,
    },
  });

  populateSelect(
    datasetSelect,
    Object.entries(DATASETS).map(([id, d]) => [id, d.label]),
    datasetId
  );
  datasetSelect.addEventListener("change", (e) => selectDataset(e.target.value).catch(showError));
  collectionSelect.addEventListener("change", (e) => selectCollection(e.target.value));
  minDateInput.addEventListener("change", (e) => {
    setMinDate(e.target.value);
    applyFilter();
  });
  minDateClear.addEventListener("click", () => {
    setMinDate("");
    applyFilter();
    minDateInput.focus();
  });
  aoiFile.addEventListener("change", (e) => {
    if (e.target.files[0]) setAoi(e.target.files[0]).catch(showError);
  });
  aoiClear.addEventListener("click", () => {
    clearAoi().catch(showError);
    aoiFile.focus();
  });

  selectDataset(datasetId).catch(showError);
});

function showError(err) {
  console.error(err);
  setStatus("triangle-alert", err.message);
  statusEl.classList.remove("skeleton");
}

// Hover highlight and click popups.
let hoveredId = null;

function setHovered(id) {
  if (id === hoveredId) return;
  if (hoveredId !== null) map.setFeatureState({ source: SOURCE, id: hoveredId }, { hover: false });
  if (id !== null) map.setFeatureState({ source: SOURCE, id }, { hover: true });
  hoveredId = id;
  map.getCanvas().style.cursor = id !== null ? "pointer" : "";
}

map.on("mousemove", "cells-fill", (e) => setHovered(e.features[0].id));
map.on("mouseleave", "cells-fill", () => setHovered(null));

map.on("click", "cells-fill", (e) => {
  const [feature] = e.features;
  const p = feature.properties;
  const t = p[collection];
  const body = `${formatDate(t)} UTC<br><span class="muted">${ageDays(t).toFixed(1)} days ago</span>`;

  new maplibregl.Popup({ closeButton: false, maxWidth: "260px" })
    .setLngLat(e.lngLat)
    .setHTML(`<strong>${featureLabel(DATASETS[datasetId].featureLabel, p)}</strong>${body}`)
    .addTo(map);
});
