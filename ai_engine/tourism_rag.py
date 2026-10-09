# tourism_rag.py — Local RAG with automatic Gemini fallback when answer is not present
import os
import logging
from llm_engine import run_llm
from retriever import retrieve, get_embedder
from languages import lang_name

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIN_SCORE = 0.25  # ignore weak matches so irrelevant context doesn't pollute the prompt


def _load_prompt():
    path = os.path.join(BASE_DIR, "prompts", "tourism_prompt.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        logger.warning("Tourism prompt missing at %s", path)
        return "You are SHIVA BOT, an expert Indian travel guide and spiritual assistant."


def _search(query, topk=5):
    try:
        qv = get_embedder().encode(query)
        return retrieve("tourism_embeds.pt", qv, k=topk, min_score=MIN_SCORE)
    except Exception as e:
        logger.warning("Retrieval error: %s", e)
        return []


def answer_tourism_rag(query, lang="en"):
    """
    1. Searches local vector database first.
    2. If match found in dataset: leverages verified local dataset facts.
    3. If NOT found in local dataset (e.g. Champawat, Almora, Chopta, etc.):
       Automatically uses Gemini API to provide complete, authentic, and rich
       travel and tourism information for that destination.
    """
    hits = _search(query, topk=5)
    valid = [t for t, _ in hits if t.strip() and t.strip() != "."]
    lname = lang_name(lang)
    base_prompt = _load_prompt()

    if valid:
        # Grounded in local verified dataset
        context = "\n\n".join(f"- {t}" for t in valid)
        system = (
            base_prompt
            + "\n\nSTRICT RULES:\n"
            + f"1. Answer ONLY in {lname}.\n"
            + "2. Prioritize the verified dataset context below for facts (state, airport, railway, attractions).\n"
            + "3. Supplement with practical travel advice: best season, realistic itineraries, transport connectivity, homestays, and eco-tips.\n"
            + "\nVerified Context from Travel Dataset:\n" + context
        )
        return run_llm(system, query, prefer="auto")
    else:
        # Destination not in local dataset -> Use Gemini API fallback
        system = (
            base_prompt
            + "\n\nSTRICT RULES:\n"
            + f"1. Answer ONLY in {lname}.\n"
            + "2. The requested place/topic is not in the local dataset. Use your comprehensive Indian tourism and geography knowledge (via Gemini) to provide a complete, detailed, and accurate travel guide for this location.\n"
            + "3. Include:\n"
            + "   • Exact Location & Geographic Overview (State, District, Altitude)\n"
            + "   • Top Places to Visit & Major Attractions (Temples, Viewpoints, Heritage sites)\n"
            + "   • How to Reach (Nearest Airport, Railway Station, and Road Route)\n"
            + "   • Best Time to Visit & Ideal Trip Duration (e.g., 2-3 Days)\n"
            + "   • Stay & Food Recommendations (Homestays, GMVN/KMVN guest houses, local Kumaoni/Garhwali/regional food)\n"
            + "   • Essential Traveler Tips & Eco-guidelines.\n"
            + "4. Structure with clear bold headings and bullet points. Never say you don't have information."
        )
        return run_llm(system, query, prefer="gemini")