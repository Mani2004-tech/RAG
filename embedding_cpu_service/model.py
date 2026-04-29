from sentence_transformers import SentenceTransformer
import numpy as np
from config import MODEL_NAME, DEVICE, BATCH_SIZE


class EmbeddingModel:

    def __init__(self):
        print("🚀 Loading BGE-M3 (CPU optimized)...")

        self.model = SentenceTransformer(
            MODEL_NAME,
            device=DEVICE
        )

        # 🔥 CPU optimization
        self.model.max_seq_length = 512

        print("✅ Model loaded")

    def embed(self, texts):

        embeddings = self.model.encode(
            texts,
            batch_size=BATCH_SIZE,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        return embeddings.tolist()