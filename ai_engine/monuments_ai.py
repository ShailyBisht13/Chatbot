import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load CLIP model once (so it's fast)
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

# List of monuments you want to classify
MONUMENTS = [
    "Taj Mahal",
    "Qutub Minar",
    "Red Fort",
    "Charminar",
    "Hawa Mahal",
    "India Gate",
    "Kedarnath Temple",
    "Badrinath Temple",
    "Somnath Temple",
    "Golden Temple",
    "Meenakshi Temple",
    "Konark Sun Temple",
    "Jagannath Puri Temple",
    "Ajanta Caves",
    "Ellora Caves",
    "Gateway of India",
    "Victoria Memorial",
    "Sanchi Stupa",
    "Khajuraho Temples",
    "Mahabodhi Temple",
    "Hampi Temples"
]

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
    "Hampi Temples": "Vijayanagara district, Karnataka, India"
}

def recognize_monument(image_path):
    """
    CLASSIFIES the input image & returns result with CLEAR confidence score & exact location.
    """

    # --------------------
    # 1. Load the image safely
    # --------------------
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        return {"error": f"Could not load image: {str(e)}"}

    # --------------------
    # 2. Run CLIP processor
    # --------------------
    inputs = processor(
        text=MONUMENTS,
        images=image,
        return_tensors="pt",
        padding=True
    )

    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)[0]

    # --------------------
    # 3. Find best match
    # --------------------
    idx = torch.argmax(probs).item()
    confidence = float(probs[idx].item())  # convert tensor → float
    mon_name = MONUMENTS[idx]
    location = MONUMENT_LOCATIONS.get(mon_name, "India")

    result = {
        "monument": mon_name,
        "location": location,
        "confidence": round(confidence * 100, 2),   # percentage format
        "raw_score": confidence                     # keep original if needed
    }

    return result
