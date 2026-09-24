# build_text_embeddings.py
from sentence_transformers import SentenceTransformer
import os, json
from dataset_loader import load_tourism_data, load_spiritual_data, load_shlokas

model = SentenceTransformer("all-MiniLM-L6-v2")  # small+fast embedder

os.makedirs("models", exist_ok=True)

def build():
    tourism = load_tourism_data()
    spiritual = load_spiritual_data()
    shlokas = load_shlokas()

    docs = []
    # tourism entries: include id so RAG can cite
    for i, t in enumerate(tourism):
        text = " | ".join([f"{k}: {v}" for k, v in t.items()])
        docs.append({"id": f"tour_{i}", "text": text})

    for i, s in enumerate(spiritual if isinstance(spiritual, list) else [spiritual]):
        if isinstance(s, dict):
            text = " | ".join([f"{k}: {v}" for k, v in s.items()])
        else:
            text = str(s)
        docs.append({"id": f"spirit_{i}", "text": text})

    for k, v in (shlokas or {}).items():
        txt = v.get("sanskrit", "") + " " + v.get("english", "")
        docs.append({"id": f"shloka_{k}", "text": txt})

    texts = [d["text"] for d in docs]
    embeddings = model.encode(texts, convert_to_numpy=True)
    # save mapping
    out = {"docs": docs, "embeddings": embeddings.tolist()}
    json.dump(out, open("models/text_embeddings.json", "w", encoding="utf-8"))
    print("Saved models/text_embeddings.json")

if __name__ == "__main__":
    build()
