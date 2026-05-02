import os
import streamlit as st
from groq import Groq

# Try Streamlit secrets first, then environment variable
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate(prompt, model="llama-3.1-8b-instant"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
