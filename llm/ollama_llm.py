import requests

def generate(prompt, model="llama3.1:8b"):
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    return res.json()["response"]