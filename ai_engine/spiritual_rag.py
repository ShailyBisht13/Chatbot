# spiritual_rag.py — Spiritual Knowledge with Local RAG and Gemini fallback
import os
import re
import logging
from llm_engine import run_llm
from retriever import retrieve, get_embedder
from languages import lang_name
from dataset_loader import load_temples

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIRITUAL_PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "spiritual_prompt.txt")
MIN_SCORE = 0.25
MAX_TEMPLES_IN_PROMPT = 8


def _load_prompt():
    try:
        with open(SPIRITUAL_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        logger.warning("Spiritual prompt missing at %s", SPIRITUAL_PROMPT_PATH)
        return "You are a spiritual guide."


SYSTEM_PROMPT = _load_prompt()


def _temple_entries(temple_data):
    """Normalise dict-or-list temple data into [(name, info_dict)]."""
    if isinstance(temple_data, dict):
        return list(temple_data.items())
    if isinstance(temple_data, list):
        return [(e.get("temple") or e.get("name") or "Unknown Temple", e) for e in temple_data]
    return []


def format_temples(temple_data, query=""):
    entries = _temple_entries(temple_data)
    q = (query or "").lower()
    relevant = [(n, i) for n, i in entries if re.search(re.escape(str(n).lower()), q)]
    if not relevant:
        return ""
    lines = []
    for name, info in relevant[:MAX_TEMPLES_IN_PROMPT]:
        lines.append(
            f"Temple: {name} | Location: {info.get('location', '')} | "
            f"Origin: {info.get('origin_story', '')} | Significance: {info.get('significance', '')} | "
            f"Best Time: {info.get('best_time_to_visit', '')}"
        )
    return "\n".join(lines)


def answer_spiritual_rag(query, lang="en", top_k=3):
    """
    1. Checks local shlokas and temple datasets.
    2. If found, grounds response in verified scriptures.
    3. If query is broader (e.g. Upanishads, Ramayana, rituals, Vedic philosophy),
       seamlessly falls back to Gemini / LLM's comprehensive spiritual knowledge.
    """
    lname = lang_name(lang)
    shl_hits = []
    try:
        q_emb = get_embedder().encode(query)
        shl_hits = retrieve("shlokas_embeds.pt", q_emb, k=top_k, min_score=MIN_SCORE)
    except Exception as e:
        logger.warning("Shloka retrieval failed: %s", e)

    shl_text = "\n".join(f"- {t[:400]}" for t, s in shl_hits) if shl_hits else ""

    temple_text = ""
    try:
        temple_text = format_temples(load_temples(), query)
    except Exception as e:
        logger.warning("Temple loading failed: %s", e)

    context_parts = []
    if shl_text:
        context_parts.append(f"Scriptural References from Dataset:\n{shl_text}")
    if temple_text:
        context_parts.append(f"Temple Heritage Details from Dataset:\n{temple_text}")

    context = "\n\n".join(context_parts)

    prompt = (
        SYSTEM_PROMPT
        + f"\n\nSTRICT RULES:\n"
        + f"1. Answer ONLY in {lname}.\n"
        + "2. Maintain a peaceful, devotional, and enlightened tone.\n"
        + "3. When explaining shlokas, provide Sanskrit text, word-by-word/line translation, and practical spiritual application for modern life.\n"
        + "4. Use clear headings and separate bullet points."
    )

    user_prompt = f"Verified Context (if relevant):\n{context}\n\nUser Question:\n{query}" if context else query
    return run_llm(prompt, user_prompt, prefer="gemini" if not context else "auto")