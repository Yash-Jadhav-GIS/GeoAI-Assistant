import geopandas as gpd
from core.spatial_ops import TOOLS


def execute(plan, gdf):
    """
    Execute a planned tool safely on a GeoDataFrame
    """

    # ---------------- VALIDATION ----------------
    if not plan or "tool" not in plan or "args" not in plan:
        raise Exception("Invalid plan format")

    tool = plan["tool"]
    args = plan["args"]

    if tool not in TOOLS:
        raise Exception(f"Invalid tool: {tool}")

    # ---------------- EXECUTION ----------------
    try:
        result = TOOLS[tool](gdf, **args)
    except Exception as e:
        raise Exception(f"[EXECUTION ERROR] Tool '{tool}' failed: {e}")

    # ---------------- NONE CHECK ----------------
    if result is None:
        raise Exception("Tool returned None")

    # ---------------- TYPE SAFETY ----------------
    if not isinstance(result, gpd.GeoDataFrame):
        try:
            # Align geometry safely using index
            result = gpd.GeoDataFrame(
                result,
                geometry=gdf.geometry.loc[result.index]
                if hasattr(result, "index") else gdf.geometry
            )
        except Exception:
            raise Exception("Result cannot be converted to GeoDataFrame")

    # ---------------- GEOMETRY SAFETY ----------------
    if "geometry" not in result.columns:
        raise Exception("No geometry column in result")

    # Remove null geometries
    result = result[result.geometry.notnull()]

    # Fix invalid geometries (common in shapefiles)
    try:
        result["geometry"] = result["geometry"].buffer(0)
    except Exception:
        pass

    if result.empty:
        raise Exception("No results found for this query")

    # ---------------- CRS SAFETY ----------------
    try:
        if result.crs is None:
            result = result.set_crs(gdf.crs)

        result = result.to_crs(4326)
    except Exception as e:
        raise Exception(f"CRS transformation failed: {e}")

    return result