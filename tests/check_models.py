import torch
import numpy as np

def check_pt(path):
    print(f"\nChecking {path}...")
    try:
        data = torch.load(path)
        print(f"Keys: {data.keys()}")
        texts = data.get("texts")
        embeddings = data.get("embeddings")
        print(f"Texts type: {type(texts)}")
        print(f"Embeddings type: {type(embeddings)}")
        if embeddings is not None:
             if hasattr(embeddings, "shape"):
                 print(f"Embeddings shape: {embeddings.shape}")
             else:
                 print(f"Embeddings has no shape attribute")
    except Exception as e:
        print(f"Error loading {path}: {e}")

check_pt("ai_engine/models/tourism_embeds.pt")
check_pt("ai_engine/models/shlokas_embeds.pt")
