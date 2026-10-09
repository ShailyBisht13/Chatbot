# retriever.py — cached, normalized vector search (NumPy)
import os
import logging
import numpy as np
import torch
from pathlib import Path

logger = logging.getLogger(__name__)
BASE = Path(__file__).resolve().parent
MODELS = BASE / "models"

_INDEX_CACHE = {}     # filename -> (texts, normalized_embeddings)
_EMBEDDER = None


def get_embedder():
    """One shared SentenceTransformer for all RAG modules (was loaded twice before).
    NOTE: if you change EMBED_MODEL, rebuild the .pt files with the SAME model."""
    global _EMBEDDER
    if _EMBEDDER is None:
        from sentence_transformers import SentenceTransformer
        _EMBEDDER = SentenceTransformer(os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2"))
    return _EMBEDDER


def _normalize(a):
    return a / (np.linalg.norm(a, axis=-1, keepdims=True) + 1e-10)


def _load_index(pt_filename):
    if pt_filename in _INDEX_CACHE:                     # <- cached: disk read happens once
        return _INDEX_CACHE[pt_filename]
    pt_path = MODELS / pt_filename
    if not pt_path.exists():
        raise FileNotFoundError(f"{pt_path} missing")
    try:
        data = torch.load(pt_path, map_location="cpu", weights_only=True)   # safe load
    except Exception as e:
        logger.warning("weights_only load failed (%s); loading as trusted local file", e)
        data = torch.load(pt_path, map_location="cpu")
    texts = list(data["texts"])
    emb = data["embeddings"]
    emb = emb.cpu().numpy() if torch.is_tensor(emb) else np.asarray(emb)
    _INDEX_CACHE[pt_filename] = (texts, _normalize(emb.astype("float32")))
    return _INDEX_CACHE[pt_filename]


def retrieve(pt_filename, query_embedding, k=5, min_score=None):
    """Return top-k [(text, cosine_score)], optionally dropping hits below min_score."""
    texts, emb = _load_index(pt_filename)
    q = query_embedding.detach().cpu().numpy() if torch.is_tensor(query_embedding) \
        else np.asarray(query_embedding)
    q = _normalize(q.reshape(-1).astype("float32"))
    sims = emb @ q                                       # (n,)
    idx = np.argsort(-sims)[:min(k, len(texts))]
    hits = [(texts[i], float(sims[i])) for i in idx]
    if min_score is not None:
        hits = [h for h in hits if h[1] >= min_score]
    return hits