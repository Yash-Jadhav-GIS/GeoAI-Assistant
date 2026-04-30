# 🌍 GeoAI Assistant — Dynamic Geospatial Query Engine

AI-powered system to **query geospatial data (GeoJSON, SHP, KML)** using natural language and visualize results instantly on an interactive map.

---

## 🚀 Demo

📸 Quick Preview:

![Map](Assist/Screenshot%202026-04-30%20114932.png)

🎥 *(Add video link here if available)*

---

## 📸 Screenshots

| Map View                                         | Query Execution                                  | EDA Dashboard                                    |
| ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
|  ![](Assist/Screenshot%202026-04-30%20115125.png)| ![](Assist/Screenshot%202026-04-30%20115010.png) |![](Assist/Screenshot%202026-04-30%20114932.png)  |

---

## ⚡ What Makes This Different?

* Works with **ANY dataset** (no predefined schema)
* Supports **natural language queries** (top, bottom, filter)
* Uses **LLM tool-calling instead of plain RAG**
* Combines **map + analytics + querying in one system**

---

## 🔥 Key Features

* 📂 Upload any geospatial dataset (Point, Line, Polygon)
* 💬 Query using natural language:

  * `top 10 by population`
  * `bottom 5 by area`
  * `filter roads > 100km`
* 🧠 Dynamic column detection (no hardcoding)
* ⚡ LLM-powered tool execution (Ollama)
* 🗺 Interactive map visualization (PyDeck)
* 📊 Built-in EDA dashboard
* 🔄 Multi-step query execution (filter → sort → visualize)

---

## 🧠 How It Works

```text
User Query
   ↓
Dynamic Parser + LLM Planner
   ↓
Tool Execution (GeoPandas)
   ↓
GeoDataFrame Output
   ↓
Map + Charts + Download
```

---

## 🏗 Project Structure

```
GeoAI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── core/
│   ├── loader.py
│   ├── spatial_ops.py
│   ├── executor.py
│   ├── map_view.py
│   ├── eda.py
│
├── llm/
│   ├── planner.py
│   ├── rag.py
│   ├── ollama_llm.py
│
├── utils/
│   ├── helpers.py
│   ├── state.py
```

---

## ⚙️ Tech Stack

* Python
* GeoPandas / Shapely
* Streamlit
* PyDeck
* Plotly
* Ollama (Local LLM)
* Schema-aware RAG

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/geoai-assistant.git
cd geoai-assistant

pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## ⚠️ Requirements

* Python 3.9+
* Ollama running locally:

```bash
ollama run llama3.1
```

---

## 🧪 Example Queries

```
top 10 by POP_EST
bottom 5 by GDP_MD
filter POP_EST > 1000000
top 5 by any numeric column
```

---

## 🎯 Use Cases

* Geospatial data exploration
* AI-powered GIS workflows
* Rapid EDA for spatial datasets
* Interactive map analytics

---

## 🚀 Future Improvements

* Advanced multi-step reasoning
* Spatial queries (buffer, intersect, nearest)
* Hybrid RAG + tool system
* Vector DB for row-level retrieval

---

## 💡 Motivation

Traditional GIS workflows are manual and tool-heavy.
This project simplifies geospatial analysis using **AI-driven querying + visualization**.

---

## 🤝 Open to Opportunities

Actively looking for roles in:

* AI / ML Engineering
* GeoAI / Geospatial AI
* Generative AI / LLM Applications

Let’s connect 🚀

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
