## Terror Incidents Map in India (1980–2025)

This code visualises major terror incidents across India from 1980 to 2025, plotted on a satellite basemap. It highlights different categories of incidents—border infiltrations, Maoist insurgencies, cross-border attacks—using colored markers pinned to their approximate locations.

Basically, it’s a **geospatial timeline** of Indian terror incidents. I needed it for a presentation I was doing and couldn't find one online. This isn't pretty (yet, hopefully) and is a bit primitive in looks and functionality, but hopefully a good starting point.

---

## What does the code do?

- Loads incident data from a CSV file (`incident_data.csv`) containing event names, years, locations, and categories.

- Converts the location names into geographic coordinates (latitude, longitude) — **hardcoded for now**, because automating geocoding reliably is a pain and would slow down this script.

- Creates a GeoDataFrame for spatial plotting using GeoPandas.

- Loads a shapefile for India’s state boundaries from a public URL.

- Projects everything into Web Mercator (EPSG:3857) for compatibility with web tile providers.

- Plots the Indian states as borders.

- Plots each incident as a colored circle, colored by its category.

- Numbers the incidents and adds a sidebar legend with incident names and years.

- Adds a satellite basemap from Esri for visual context.

- Saves the plot as a high-res PNG image (`satellite_terror_map.png`).

---

## What does it use?

- **Python 3.x**

- `pandas` — For tabular data handling

- `geopandas` — For spatial data and map plotting

- `matplotlib` — For plotting the map and markers

- `shapely` — To work with geographic shapes and points

- `contextily` — To add the satellite basemap tiles

- `descartes` — Needed by GeoPandas for plotting geometries

- `pyproj` — For coordinate reference system transformations

- `numpy` — For general numerical operations

---

## How to run

1. Clone the repo.

2. Create a Python environment and install dependencies:

```bash
pip install -r requirements.txt

```
3. Run the script: `plot_map.py`

