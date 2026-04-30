import json
import re

from llm.ollama_llm import generate
from llm.rag import get_context


# ---------------- HELPERS ----------------
def extract_number(query):
    match = re.search(r"\b(\d+)\b", query)
    return int(match.group(1)) if match else 5


def find_closest_column(word, columns):
    word = word.lower()
    for col in columns:
        if word in col.lower():
            return col
    return None


def get_numeric_columns(columns, gdf=None):
    if gdf is None:
        return []

    return [
        col for col in columns
        if str(gdf[col].dtype) in ["int64", "float64"]
    ]


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


# ---------------- FALLBACK (SMART) ----------------
def fallback_plan(query, columns, gdf=None):
    q = query.lower()
    n = extract_number(query)
    numeric_cols = get_numeric_columns(columns, gdf)

    # -------- MULTI-STEP: FILTER + TOP --------
    if ("top" in q or "highest" in q) and "in" in q:
        # Example: "top 5 countries in Asia"
        for col in columns:
            if col.lower() in q:
                return {
                    "tool": "top_n_by_column",
                    "args": {"column": col, "n": n}
                }

    # -------- TOP --------
    if "top" in q or "highest" in q or "largest" in q:
        for col in columns:
            if col.lower() in q:
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
            value = float(parts[1].strip())

            col = find_closest_column(col_word, columns)

            if col:
                return {
                    "tool": "filter_greater",
                    "args": {"column": col, "value": value}
                }
        except:
            pass

    return None


# ---------------- MAIN PLANNER ----------------
def plan(query, columns, gdf=None):

    context = get_context(query)
    n = extract_number(query)

    prompt = f"""
You are a GeoAI planner.

Columns:
{columns}

Context:
{context}

Available tools:
- filter_equals(column, value)
- filter_greater(column, value)
- top_n_by_column(column, n)
- group_count(column)
- area_filter(min_area)
- buffer(distance)
- top_n_per_group(group_col, value_col, n)

STRICT RULES:
- Return ONLY JSON
- Extract number from query (e.g. "top 15" → n=15)
- Use ONLY given column names
- Prefer numeric columns for ranking
- Do not hallucinate

Format:
{{
  "tool": "tool_name",
  "args": {{}}
}}

Query: {query}
"""

    response = generate(prompt)

    # ---------------- LLM PARSE ----------------
    json_str = extract_json(response)

    if json_str:
        try:
            plan_json = json.loads(json_str)
        except:
            plan_json = None
    else:
        plan_json = None

    # ---------------- VALIDATION ----------------
    if plan_json and "tool" in plan_json and "args" in plan_json:

        args = plan_json["args"]

        # Fix columns
        for key, value in args.items():
            if "col" in key or key == "column":
                if value not in columns:
                    fixed = find_closest_column(value, columns)
                    if fixed:
                        args[key] = fixed

        # Force correct n from query
        if "n" in args:
            args["n"] = n

        plan_json["args"] = args
        return plan_json

    # ---------------- FALLBACK ----------------
    return fallback_plan(query, columns, gdf)