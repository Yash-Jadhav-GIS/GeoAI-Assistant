import geopandas as gpd


# ---------------- VALIDATION ----------------
def validate_column(gdf, column):
    if column not in gdf.columns:
        raise Exception(f"Column not found: {column}")


# ---------------- FILTER EQUALS ----------------
def filter_equals(gdf, column, value):
    validate_column(gdf, column)
    return gdf[gdf[column] == value].copy()


# ---------------- FILTER GREATER ----------------
def filter_greater(gdf, column, value):
    validate_column(gdf, column)
    return gdf[gdf[column] > float(value)].copy()


# ---------------- TOP / BOTTOM ----------------
def top_n_by_column(gdf, column, n=5, order="desc"):
    validate_column(gdf, column)

    n = int(n)

    try:
        if order == "asc":
            return gdf.nsmallest(n, column).copy()   # 🔥 bottom
        else:
            return gdf.nlargest(n, column).copy()    # 🔥 top
    except Exception as e:
        raise Exception(f"Sorting failed: {e}")


# ---------------- LEGACY TOP N ----------------
def top_n(gdf, column, n=5):
    return top_n_by_column(gdf, column, n, order="desc")


# ---------------- GROUP COUNT ----------------
def group_count(gdf, column):
    validate_column(gdf, column)

    df = gdf.groupby(column).size().reset_index(name="count")

    # keep geometry (important for map rendering)
    return gdf.merge(df, on=column, how="left")


# ---------------- AREA FILTER ----------------
def area_filter(gdf, min_area):
    projected = gdf.to_crs(3857)
    mask = projected.geometry.area > float(min_area)
    return gdf[mask].copy()


# ---------------- BUFFER ----------------
def buffer(gdf, distance):
    gdf_copy = gdf.copy()
    gdf_copy["geometry"] = gdf_copy.geometry.buffer(float(distance))
    return gdf_copy


# ---------------- TOP N PER GROUP ----------------
def top_n_per_group(gdf, group_col, value_col, n=5):
    validate_column(gdf, group_col)
    validate_column(gdf, value_col)

    return (
        gdf.sort_values(value_col, ascending=False)
        .groupby(group_col)
        .head(int(n))
        .copy()
    )


# ---------------- TOOL REGISTRY ----------------
TOOLS = {
    "filter_equals": filter_equals,
    "filter_greater": filter_greater,
    "top_n": top_n,
    "top_n_by_column": top_n_by_column,   # ✅ FIXED
    "group_count": group_count,
    "area_filter": area_filter,
    "buffer": buffer,
    "top_n_per_group": top_n_per_group,
}