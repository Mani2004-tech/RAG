# import requests
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity

# from config.config import EMBEDDING_ENDPOINT


# class SemanticChunker:

#     def __init__(self, threshold=0.75):

#         self.threshold = threshold
#         self.endpoint = EMBEDDING_ENDPOINT

#     # -----------------------------
#     # Embedding API
#     # -----------------------------
#     def get_embeddings(self, texts):

#         payload = {
#             "texts": texts
#         }

#         response = requests.post(
#             self.endpoint,
#             json=payload,
#             timeout=60
#         )

#         data = response.json()

#         # expected format: {"embeddings":[...]}
#         return np.array(data["embeddings"])

#     # -----------------------------
#     # Semantic Chunking
#     # -----------------------------
#     def chunk(self, sentences):

#         if not sentences:
#             return []

#         embeddings = self.get_embeddings(sentences)

#         chunks = []
#         current_chunk = [sentences[0]]

#         for i in range(1, len(sentences)):

#             sim = cosine_similarity(
#                 [embeddings[i - 1]],
#                 [embeddings[i]]
#             )[0][0]

#             if sim < self.threshold:

#                 chunks.append(" ".join(current_chunk))
#                 current_chunk = []

#             current_chunk.append(sentences[i])

#         if current_chunk:
#             chunks.append(" ".join(current_chunk))

#         return chunks
from langsmith import traceable
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from config.config import EMBEDDING_ENDPOINT


class SemanticChunker:

    def __init__(self, threshold=0.75):

        self.threshold = threshold
        self.endpoint = EMBEDDING_ENDPOINT

    @traceable(name="semantic_get_embeddings", run_type="tool")
    def get_embeddings(self, texts):

        payload = {
            "texts": texts
        }

        response = requests.post(
            self.endpoint,
            json=payload,
            timeout=60
        )

        data = response.json()

        return np.array(data["embeddings"])

    @traceable(name="semantic_chunking", run_type="chain")
    def chunk(self, sentences):

        if not sentences:
            return []

        embeddings = self.get_embeddings(sentences)

        chunks = []
        current_chunk = [sentences[0]]

        for i in range(1, len(sentences)):

            sim = cosine_similarity(
                [embeddings[i - 1]],
                [embeddings[i]]
            )[0][0]

            if sim < self.threshold:

                chunks.append(" ".join(current_chunk))
                current_chunk = []

            current_chunk.append(sentences[i])

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks