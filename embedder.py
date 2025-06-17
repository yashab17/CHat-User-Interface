from sentence_transformers import SentenceTransformer
from PIL import Image
import os

class EmbeddingProcessor:
    def __init__(self, model_name="clip-ViT-L-14"):
        # Load a model that can embed both text and images
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text):
        """
        Embed a single piece of text.
        """
        return self.model.encode(text, normalize_embeddings=True)

    def embed_image(self, image_path):
        """
        Embed a single image.
        """
        img = Image.open(image_path).convert("RGB").resize((224, 224))
        return self.model.encode([img], normalize_embeddings=True)[0]
