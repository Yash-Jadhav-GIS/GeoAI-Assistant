import pydeck as pdk
import geopandas as gpd


# 🎨 Color themes
COLOR_THEMES = {
    "red": [255, 0, 0, 140],
    "blue": [0, 123, 255, 140],
    "green": [40, 167, 69, 140],
    "orange": [255, 165, 0, 140],
    "purple": [111, 66, 193, 140],
    "cyan": [23, 162, 184, 140],
    "yellow": [255, 193, 7, 140]
}


# ---------------- CLEAN GEO ----------------
def clean_gdf(gdf):
    if gdf is None or gdf.empty:
        return None

    if not isinstance(gdf, gpd.GeoDataFrame):
        return None

    if "geometry" not in gdf.columns:
        return None

    gdf = gdf[gdf.geometry.notnull()]

    if gdf.empty:
        return None

    if gdf.crs is None:
        gdf = gdf.set_crs(4326)

    return gdf.to_crs(4326)


# ---------------- ZOOM TO BOUNDS ----------------
def get_bounds_view(gdf):
    try:
        bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]

        center_lon = (bounds[0] + bounds[2]) / 2
        center_lat = (bounds[1] + bounds[3]) / 2

        # approximate zoom logic
        lon_diff = bounds[2] - bounds[0]
        lat_diff = bounds[3] - bounds[1]
        max_diff = max(lon_diff, lat_diff)

        if max_diff < 0.01:
            zoom = 12
        elif max_diff < 0.1:
            zoom = 10
        elif max_diff < 1:
            zoom = 8
        elif max_diff < 10:
            zoom = 5
        else:
            zoom = 3

        return float(center_lat), float(center_lon), zoom

    except:
        return 20.5937, 78.9629, 3  # fallback


# ---------------- TOOLTIP ----------------
def build_tooltip(gdf):
    cols = [c for c in gdf.columns if c != "geometry"][:5]

    html = ""
    for col in cols:
        html += f"<b>{col}:</b> {{{col}}}<br>"

    return {"html": html}


# ---------------- LAYER BUILDER ----------------
def build_layer(gdf, color, is_base=False):
    geom_type = gdf.geometry.iloc[0].geom_type

    if geom_type in ["Point", "MultiPoint"]:
        return pdk.Layer(
            "ScatterplotLayer",
            gdf,
            get_position="[geometry.coordinates[0], geometry.coordinates[1]]",
            get_fill_color=color if not is_base else [150, 150, 150, 50],
            get_radius=5000,
            pickable=True
        )

    elif geom_type in ["LineString", "MultiLineString"]:
        return pdk.Layer(
            "GeoJsonLayer",
            gdf.__geo_interface__,
            stroked=True,
            filled=False,
            get_line_color=color if not is_base else [150, 150, 150],
            line_width_min_pixels=2,
            pickable=True
        )

    else:  # Polygon
        return pdk.Layer(
            "GeoJsonLayer",
            gdf.__geo_interface__,
            filled=True,
            stroked=True,
            get_fill_color=color if not is_base else [150, 150, 150, 30],
            get_line_color=[0, 0, 0],
            line_width_min_pixels=1,
            pickable=True
        )


# ---------------- MAIN MAP ----------------
def render_map(base_gdf, filtered_gdf, color="red"):

    base_gdf = clean_gdf(base_gdf)
    filtered_gdf = clean_gdf(filtered_gdf)

    if filtered_gdf is None:
        return pdk.Deck()

    fill_color = COLOR_THEMES.get(color, COLOR_THEMES["red"])

    layers = []

    # Base layer (light background)
    if base_gdf is not None:
        layers.append(build_layer(base_gdf, [150, 150, 150, 40], is_base=True))

    # Highlight layer
    layers.append(build_layer(filtered_gdf, fill_color))

    # View
    lat, lon, zoom = get_bounds_view(filtered_gdf)

    view = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=zoom,
    )

    tooltip = build_tooltip(filtered_gdf)

    return pdk.Deck(
        layers=layers,
        initial_view_state=view,
        tooltip=tooltip,
    )