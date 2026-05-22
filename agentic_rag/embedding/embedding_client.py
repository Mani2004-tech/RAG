import requests

from agentic_rag.config.config import EMBEDDING_ENDPOINT


class EmbeddingClient:

    def embed(self, texts):
        payload = {"texts": texts}
        response = requests.post(EMBEDDING_ENDPOINT, json=payload)
        data = response.json()
        return data["embeddings"]
