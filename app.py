import streamlit as st
import plotly.express as px
import re

from core.loader import load_file
from core.map_view import render_map
from core.eda import summary, geometry_stats, missing_values, data_preview
from core.executor import execute

from llm.planner import plan
from llm.rag import index_schema

from utils.state import init_state
from utils.helpers import download_geojson


# ---------------- CONFIG ----------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 GeoAI Assistant (Dynamic GeoAI Engine)")


# ---------------- HELPERS ----------------
def extract_n(query):
    match = re.search(r"\b(\d+)\b", query)
    return int(match.group(1)) if match else 5


def get_numeric_columns(gdf):
    return [
        col for col in gdf.columns
        if gdf[col].dtype in ["int64", "float64"]
    ]


def find_column_from_query(query, columns):
    q = query.lower()
    for col in columns:
        if col.lower() in q:
            return col
    return None


# ---------------- DYNAMIC PARSER ----------------
def parse_dynamic_query(query, gdf):
    q = query.lower()
    columns = list(gdf.columns)
    numeric_cols = get_numeric_columns(gdf)

    n = extract_n(query)

    # -------- TOP --------
    if "top" in q or "highest" in q:
        col = find_column_from_query(query, columns)

        if col:
            return {
                "tool": "top_n_by_column",
                "args": {"column": col, "n": n}
            }

        if numeric_cols:
            return {
                "tool": "top_n_by_column",
                "args": {"column": numeric_cols[0], "n": n}
            }

    # -------- FILTER --------
    if ">" in q:
        try:
            parts = q.split(">")
            col_word = parts[0].strip().split()[-1]
            val = float(parts[1].strip())

            col = find_column_from_query(col_word, columns)

            if col:
                return {
                    "tool": "filter_greater",
                    "args": {"column": col, "value": val}
                }
        except:
            pass

    return None


# ---------------- FILE UPLOAD ----------------
file = st.file_uploader("Upload Geo Data (GeoJSON / KML / SHP ZIP)")

if file:
    try:
        gdf = load_file(file).to_crs(4326)

        init_state(gdf)
        index_schema(gdf)

        base = st.session_state.original
        data = st.session_state.filtered

        # Store last result separately
        if "result_data" not in st.session_state:
            st.session_state.result_data = data

        st.caption(f"Columns: {list(data.columns)}")

        col1, col2 = st.columns([4, 1], gap="small")

        # ---------------- MAP ----------------
        with col1:
            color = st.selectbox(
                "🎨 Highlight Color",
                ["red", "blue", "green", "orange", "purple", "cyan", "yellow"]
            )

            st.pydeck_chart(
                render_map(base, data, color),
                use_container_width=True,
                height=450
            )

        # ---------------- EDA ----------------
        with col2:
            stats = summary(data)

            st.metric("Rows", stats["rows"])
            st.metric("Columns", stats["num_columns"])

            geom_df = geometry_stats(data)
            if not geom_df.empty:
                fig = px.bar(geom_df, x="geometry_type", y="count", height=200)
                st.plotly_chart(fig, use_container_width=True)

        # ---------------- QUERY ----------------
        st.markdown("### 💬 Ask your data")
        query = st.text_input("Example: top 15 by any column")

        if query:
            with st.spinner("Processing..."):

                plan_json = parse_dynamic_query(query, data)

                if not plan_json:
                    plan_json = plan(query, list(base.columns), data)

            st.json(plan_json)

            if plan_json:
                try:
                    result = execute(plan_json, data)

                    # store result but DON'T update map yet
                    st.session_state.result_data = result

                    st.success(f"{len(result)} records ready")

                except Exception as e:
                    st.error(f"Execution failed: {e}")

        # ---------------- ACTION BUTTONS ----------------
        colA, colB, colC = st.columns(3)

        with colA:
            if st.button("🗺 Show on Map"):
                st.session_state.filtered = st.session_state.result_data

        with colB:
            st.download_button(
                "⬇ Download Result",
                download_geojson(st.session_state.result_data),
                file_name="result.geojson"
            )

        with colC:
            if st.button("🔄 Reset"):
                st.session_state.filtered = st.session_state.original

        # ---------------- PREVIEW ----------------
        st.markdown("### 📄 Result Preview")
        st.dataframe(data_preview(st.session_state.result_data), use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")