# monuments_helper.py
import torch
from sentence_transformers import SentenceTransformer, util
from PIL import Image

data = torch.load("models/clip_text_embeds.pt")
labels = data["labels"]
text_embeds = data["embeddings"]  # tensor

model = SentenceTransformer("clip-ViT-B-32")

def recognize_monument(image_path):
    image = Image.open(image_path).convert("RGB")
    img_emb = model.encode(image, convert_to_tensor=True)
    scores = util.cos_sim(img_emb, text_embeds)[0]
    best = int(scores.argmax())
    return {"label": labels[best], "score": float(scores[best])}
