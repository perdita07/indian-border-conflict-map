import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from matplotlib.patches import Rectangle
import matplotlib.patheffects as PathEffects
import numpy as np
import contextily as ctx

# === INCIDENT DATA ===
df = pd.read_csv("incident_data.csv") 

# === GEOLOCATION ===
coordinates = {
    "Tripura, India": (23.9408, 91.9882),
    "Assam, India": (26.2006, 92.9376),
    "Dhemaji, Assam, India": (27.4728, 94.5815),
    "Dimapur, Nagaland, India": (25.9044, 93.7267),
    "Malegaon, Maharashtra, India": (20.5579, 74.5287),
    "Panipat, Haryana, India": (29.3909, 76.9635),
    "Mumbai, Maharashtra, India": (19.0760, 72.8777),
    "Gandhinagar, Gujarat, India": (23.2156, 72.6369),
    "Srinagar, Jammu and Kashmir, India": (34.0837, 74.7973),
    "New Delhi, Delhi, India": (28.7041, 77.1025),
    "Jammu, Jammu and Kashmir, India": (32.7266, 74.8570),
    "Pulwama, Jammu and Kashmir, India": (33.8700, 74.9300),
    "Pathankot, Punjab, India": (32.2684, 75.6473),
    "Uri, Jammu and Kashmir, India": (34.0890, 74.3640),
    "Baramulla, Jammu and Kashmir, India": (34.2090, 74.3440),
    "Handwara, Jammu and Kashmir, India": (34.4037, 74.2749),
    "Nagrota, Jammu and Kashmir, India": (32.8340, 74.9370),
    "Awantipora, Jammu and Kashmir, India": (33.9211, 75.1300),
    "Rajouri, Jammu and Kashmir, India": (33.3775, 74.3150),
    "Reasi, Jammu and Kashmir, India": (33.0839, 74.8300),
    "Pahalgam, Jammu and Kashmir, India": (34.0144, 75.3312),
    "Dantewada, Chhattisgarh, India": (18.9026, 81.3545),
    "Sukma, Chhattisgarh, India": (18.3881, 81.6711),
}

latitudes = [coordinates[loc][0] for loc in df["Location"]]
longitudes = [coordinates[loc][1] for loc in df["Location"]]
df["Latitude"] = latitudes
df["Longitude"] = longitudes
geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
geo_df = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# === CATEGORY COLORS ===
category_colors = {
    'Border Infiltration': '#e74c3c',
    'Border District Terror': '#e67e22',
    'Northeast Border Zone': '#f39c12',
    'Cross-border Terror Links': '#d35400',
    'Cross-border Train Attack': '#8e44ad',
    'Coastal Infiltration': '#3498db',
    'Border Proximity': '#2ecc71',
    'Cross-border Extremists': '#c0392b',
    'Border Zone Attack': '#e74c3c',
    'Line-of-Control Infiltration': '#a93226',
    'Border Sector Attack': '#922b21',
    'Border Infiltration Zone': '#7b241c',
    'Border-Proximate Military Installation': '#641e16',
    'Terrorist Infiltration': '#5d1a1b',
    'Cross-border Planning': '#512e5f',
    'Cross-border Fire Exchange': '#4a235a',
    'Border Terrorism': '#ff6b6b',
    'Border-Periphery Terror': '#ee5a24',
    'Border-Linked Attack': '#ff9ff3',
    'Maoist Insurgency': '#f368e0',
    'Maoist Jungle Ambush': '#ff3838',
    'Dense Border Forest Ambush': '#ff9f43',
    'Repeat Insurgency Zone': '#7bed9f'
}

# === INDIA MAP DATA ===
url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson"
india = gpd.read_file(url).set_crs("EPSG:4326")

# === PROJECTION TO WEB MERCATOR ===
india = india.to_crs(epsg=3857)
geo_df = geo_df.to_crs(epsg=3857)

# === PLOT ===
fig, ax = plt.subplots(figsize=(14, 16))
fig.patch.set_facecolor("#f4f4f4")

# Plot India state borders
india.plot(ax=ax, color='none', edgecolor='black', linewidth=2.5, zorder=1)

# Plot incidents
geo_df = geo_df.sort_values(by="Year").reset_index(drop=True)
for idx, row in geo_df.iterrows():
    category_color = category_colors.get(row['Category'], '#888')
    ax.plot(row.geometry.x, row.geometry.y,
            marker='o', markersize=11, color=category_color,
            markeredgecolor='black', markeredgewidth=0.6, alpha=0.88, zorder=5)

    ax.plot(row.geometry.x, row.geometry.y,
            marker='o', markersize=7, color='#111', alpha=0.95, zorder=6)

    txt = ax.text(row.geometry.x, row.geometry.y, str(idx + 1),
                  fontsize=8.5, ha='center', va='center', color='white',
                  weight='bold', zorder=7)
    txt.set_path_effects([PathEffects.withStroke(linewidth=1.8, foreground='black')])

# Add satellite basemap
ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, zoom=5)

# Final touches
ax.set_xlim(india.total_bounds[[0, 2]])
ax.set_ylim(india.total_bounds[[1, 3]])
ax.axis("off")

# Title
title = ax.set_title("Terror Incidents in India (1980–2025)\nBorder, Infiltration, and Maoist-Affected Zones",
                     fontsize=20, weight="bold", pad=20, color='white')
title.set_path_effects([PathEffects.withStroke(linewidth=2.5, foreground='black')])

# Incident index
legend_text = ""
for idx, row in geo_df.iterrows():
    name = row['Event']
    if len(name) > 30:
        name = name[:28] + '…'
    legend_text += f"{idx+1:2d}. {name} ({row['Year']})\n"

plt.figtext(0.82, 0.45, "Incident Index",
            fontsize=10, weight='bold', ha='left', color='white')
plt.figtext(0.82, 0.43, legend_text,
            fontsize=7, ha='left', va='top', linespacing=1.2,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#000", edgecolor="#ccc", alpha=0.6))

plt.tight_layout()
plt.subplots_adjust(right=0.8)
plt.savefig("satellite_terror_map.png", dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
