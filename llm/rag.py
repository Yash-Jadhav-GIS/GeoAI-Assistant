import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()

# Using default embedding - no Ollama needed, works on Streamlit Cloud
embed = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="geo_schema",
    embedding_function=embed
)

def index_schema(gdf):
    docs = [f"{col}: {gdf[col].dtype}" for col in gdf.columns]
    ids = [str(i) for i in range(len(docs))]
    collection.upsert(documents=docs, ids=ids)

def get_context(query):
    res = collection.query(query_texts=[query], n_results=3)
    return res["documents"][0]
