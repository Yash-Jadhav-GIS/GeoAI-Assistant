import pandas as pd
import geopandas as gpd


# ---------------- BASIC SUMMARY ----------------
def summary(gdf):
    return {
        "rows": len(gdf),
        "columns": list(gdf.columns),
        "num_columns": len(gdf.columns),
        "geom_types": gdf.geometry.geom_type.value_counts().to_dict(),
    }


# ---------------- COLUMN TYPES ----------------
def column_types(gdf):
    return {
        "numeric": list(gdf.select_dtypes(include=["int64", "float64"]).columns),
        "categorical": list(gdf.select_dtypes(include=["object"]).columns),
        "datetime": list(gdf.select_dtypes(include=["datetime"]).columns),
    }


# ---------------- MISSING VALUES ----------------
def missing_values(gdf):
    df = gdf.isnull().sum().reset_index()
    df.columns = ["column", "missing_count"]
    df["missing_pct"] = (df["missing_count"] / len(gdf)) * 100
    return df.sort_values("missing_count", ascending=False)


# ---------------- GEOMETRY STATS ----------------
def geometry_stats(gdf):
    geom_counts = gdf.geometry.geom_type.value_counts().reset_index()
    geom_counts.columns = ["geometry_type", "count"]
    return geom_counts


# ---------------- NUMERIC STATS ----------------
def numeric_summary(gdf):
    numeric_df = gdf.select_dtypes(include=["int64", "float64"])
    if numeric_df.empty:
        return pd.DataFrame()

    return numeric_df.describe().T.reset_index().rename(columns={"index": "column"})


# ---------------- CATEGORY STATS ----------------
def categorical_summary(gdf, col):
    if col not in gdf.columns:
        return pd.DataFrame()

    if gdf[col].dtype != "object":
        return pd.DataFrame()

    return (
        gdf[col]
        .value_counts()
        .reset_index()
        .rename(columns={"index": col, col: "count"})
        .head(10)
    )


# ---------------- NUMERIC DISTRIBUTION ----------------
def numeric_distribution(gdf, col):
    if col not in gdf.columns:
        return pd.Series()

    if gdf[col].dtype not in ["int64", "float64"]:
        return pd.Series()

    return gdf[col]


# ---------------- DATA PREVIEW ----------------
def data_preview(gdf, n=10):
    return gdf.head(n)