# ai_engine/retriever.py
import os
import numpy as np
from pathlib import Path
import torch

BASE = Path(__file__).resolve().parent
MODELS = BASE / "models"

def _cosine(a, b):
    # a: (n,d), b: (m,d) -> (n,m)
    an = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-10)
    bn = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return an @ bn.T

def build_index_from_pt(pt_path):
    data = torch.load(pt_path)
    texts = data["texts"]
    emb = data["embeddings"].cpu().numpy()
    return texts, emb

def retrieve(pt_filename, query_embedding, k=5):
    """
    pt_filename e.g. 'tourism_embeds.pt' in models/
    query_embedding: numpy array (d,) or torch tensor
    returns list of (text, score)
    """
    pt_path = MODELS / pt_filename
    if not pt_path.exists():
        raise FileNotFoundError(f"{pt_path} missing")
    texts, emb = build_index_from_pt(pt_path)
    if torch.is_tensor(query_embedding):
        q = query_embedding.cpu().numpy()
    else:
        q = np.array(query_embedding)
    q = q.reshape(1, -1)
    sims = _cosine(emb, q).squeeze()  # (n,)
    idx = np.argsort(-sims)[:k]
    return [(texts[i], float(sims[i])) for i in idx]
