# monuments_ai.py — CLIP zero-shot monument recognition with strict non-monument rejection
import os
import logging
import torch
from PIL import Image

logger = logging.getLogger(__name__)
CLIP_MODEL = os.getenv("CLIP_MODEL", "openai/clip-vit-large-patch14")
MIN_CONFIDENCE = 50.0  # Require >= 50% confidence to claim a monument match

MONUMENT_LOCATIONS = {
    "Taj Mahal": "Agra, Uttar Pradesh, India",
    "Qutub Minar": "Mehrauli, New Delhi, India",
    "Red Fort": "Old Delhi, New Delhi, India",
    "Charminar": "Hyderabad, Telangana, India",
    "Hawa Mahal": "Jaipur, Rajasthan, India",
    "India Gate": "Rajpath, New Delhi, India",
    "Kedarnath Temple": "Rudraprayag district, Uttarakhand, India",
    "Badrinath Temple": "Chamoli district, Uttarakhand, India",
    "Somnath Temple": "Prabhas Patan, Veraval, Gujarat, India",
    "Golden Temple": "Amritsar, Punjab, India",
    "Meenakshi Temple": "Madurai, Tamil Nadu, India",
    "Konark Sun Temple": "Konark, Puri district, Odisha, India",
    "Jagannath Puri Temple": "Puri, Odisha, India",
    "Ajanta Caves": "Chhatrapati Sambhajinagar (Aurangabad), Maharashtra, India",
    "Ellora Caves": "Chhatrapati Sambhajinagar (Aurangabad), Maharashtra, India",
    "Gateway of India": "Mumbai, Maharashtra, India",
    "Victoria Memorial": "Kolkata, West Bengal, India",
    "Sanchi Stupa": "Raisen district, Madhya Pradesh, India",
    "Khajuraho Temples": "Chhatarpur district, Madhya Pradesh, India",
    "Mahabodhi Temple": "Bodh Gaya, Bihar, India",
    "Hampi Temples": "Vijayanagara district, Karnataka, India",
}
MONUMENTS = list(MONUMENT_LOCATIONS.keys())

# Negative labels: If one of these wins or confidence is low, it is definitely NOT a monument
NEGATIVE_LABELS = [
    "a photo of a person doing yoga or exercise",
    "a photo of a person or a selfie",
    "a photo of human body, face, or hands",
    "a photo of an animal, bird, or pet",
    "a photo of food, dish, or beverage",
    "a photo of an ordinary room, house, indoor furniture, or street",
    "a photo of a random landscape, trees, mountain, or nature scene",
    "a screenshot, diagram, document, or text",
]
PROMPTS = [f"a photo of the {m}, a famous monument in India" for m in MONUMENTS] + NEGATIVE_LABELS

_model = _processor = None


def _load():
    """Lazy load CLIP model on demand."""
    global _model, _processor
    if _model is None:
        from transformers import CLIPModel, CLIPProcessor

        _model = CLIPModel.from_pretrained(CLIP_MODEL).eval()
        _processor = CLIPProcessor.from_pretrained(CLIP_MODEL)
    return _model, _processor


def recognize_monument(image_path):
    """
    Classifies whether the image is a known Indian monument or NOT a monument.
    Returns:
      - {"is_monument": True, "monument": name, "location": location, "confidence": float}
      - {"is_monument": False, "reason": "not_a_monument", "confidence": float}
    """
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        return {"is_monument": False, "error": f"Could not load image: {e}"}

    try:
        model, processor = _load()
        inputs = processor(text=PROMPTS, images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            probs = model(**inputs).logits_per_image.softmax(dim=1)[0]

        idx = int(torch.argmax(probs))
        confidence = round(float(probs[idx]) * 100, 2)

        # 1. If a negative label won (person, yoga pose, selfie, food, indoor room, etc.)
        if idx >= len(MONUMENTS):
            negative_label = NEGATIVE_LABELS[idx - len(MONUMENTS)]
            logger.info("Image identified as negative label: %s (%s%%)", negative_label, confidence)
            return {
                "is_monument": False,
                "reason": "not_a_monument",
                "detected_type": negative_label,
                "confidence": confidence,
            }

        # 2. If confidence is too low (< MIN_CONFIDENCE)
        if confidence < MIN_CONFIDENCE:
            logger.info("Low confidence monument match: %s%%", confidence)
            return {
                "is_monument": False,
                "reason": "low_confidence",
                "confidence": confidence,
            }

        # 3. High confidence genuine monument match
        name = MONUMENTS[idx]
        return {
            "is_monument": True,
            "monument": name,
            "location": MONUMENT_LOCATIONS.get(name, "India"),
            "confidence": confidence,
            "raw_score": float(probs[idx]),
        }

    except Exception as e:
        logger.warning("CLIP monument recognition error: %s", e)
        return {"is_monument": False, "error": str(e)}