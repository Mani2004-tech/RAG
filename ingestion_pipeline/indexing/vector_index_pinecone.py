# # # from pinecone import Pinecone
# # # from embedding.embedding_client import EmbeddingClient
# # # from config.config import PINECONE_API_KEY, PINECONE_INDEX


# # # class PineconeVectorIndex:

# # #     def __init__(self):

# # #         self.pc = Pinecone(api_key=PINECONE_API_KEY)
# # #         self.index = self.pc.Index(PINECONE_INDEX)

# # #         self.embedder = EmbeddingClient()

# # #     def index_chunks(self, chunks, batch_size=50):

# # #         if not chunks:
# # #             print("⚠ No chunks for indexing")
# # #             return

# # #         embeddings = self.embedder.embed(chunks)

# # #         vectors = []

# # #         for i, emb in enumerate(embeddings):

# # #             vectors.append({
# # #                 "id": str(i),
# # #                 "values": emb,
# # #                 "metadata": {"text": chunks[i]}
# # #             })

# # #         # -----------------------------
# # #         # Batch Upsert
# # #         # -----------------------------
# # #         for i in range(0, len(vectors), batch_size):

# # #             batch = vectors[i:i + batch_size]

# # #             print(f"Indexing batch {i//batch_size + 1}")

# # #             self.index.upsert(vectors=batch)

# # # from pinecone import Pinecone
# # # from embedding.embedding_client import EmbeddingClient
# # # from config.config import PINECONE_API_KEY, PINECONE_INDEX


# # # class PineconeVectorIndex:

# # #     def __init__(self):

# # #         print("🌲 Initializing Pinecone Vector Index")

# # #         self.pc = Pinecone(api_key=PINECONE_API_KEY)
# # #         self.index = self.pc.Index(PINECONE_INDEX)

# # #         self.embedder = EmbeddingClient()

# # #         print("✅ Pinecone index ready")

# # #     def index_chunks(self, chunks, batch_size=50):

# # #         if not chunks:
# # #             print("⚠ No chunks for indexing")
# # #             return

# # #         print(f"🧠 Generating embeddings for {len(chunks)} chunks")

# # #         embeddings = self.embedder.embed(chunks)

# # #         vectors = []

# # #         for i, emb in enumerate(embeddings):

# # #             vectors.append({
# # #                 "id": str(i),
# # #                 "values": emb,
# # #                 "metadata": {"text": chunks[i]}
# # #             })

# # #         print(f"📦 Upserting {len(vectors)} vectors to Pinecone")

# # #         for i in range(0, len(vectors), batch_size):

# # #             batch = vectors[i:i + batch_size]

# # #             print(f"🚀 Pinecone batch {i//batch_size + 1}")

# # #             self.index.upsert(vectors=batch)

# # #         print("✅ Pinecone indexing complete")

# # from pinecone import Pinecone
# # from embedding.embedding_client import EmbeddingClient
# # from config.config import PINECONE_API_KEY, PINECONE_INDEX


# # class PineconeVectorIndex:

# #     def __init__(self):

# #         print("🌲 Initializing Pinecone Vector Index")

# #         # Initialize client
# #         self.pc = Pinecone(api_key=PINECONE_API_KEY)

# #         # Connect to index
# #         self.index = self.pc.Index(PINECONE_INDEX)

# #         self.embedder = EmbeddingClient()

# #         print("✅ Pinecone index ready")

# #     def index_chunks(self, chunks, batch_size=50):

# #         if not chunks:
# #             print("⚠ No chunks for indexing")
# #             return

# #         print(f"🧠 Generating embeddings for {len(chunks)} chunks")

# #         embeddings = self.embedder.embed(chunks)

# #         vectors = []

# #         for i, emb in enumerate(embeddings):

# #             vectors.append({
# #                 "id": f"chunk-{i}",
# #                 "values": emb,
# #                 "metadata": {
# #                     "text": chunks[i]
# #                 }
# #             })

# #         print(f"📦 Upserting {len(vectors)} vectors to Pinecone")

# #         for i in range(0, len(vectors), batch_size):

# #             batch = vectors[i:i + batch_size]

# #             print(f"🚀 Pinecone batch {i//batch_size + 1}")

# #             self.index.upsert(vectors=batch)

# #         print("✅ Pinecone indexing complete")

# import uuid
# from concurrent.futures import ThreadPoolExecutor

# from pinecone import Pinecone
# from embedding.embedding_client import EmbeddingClient
# from config.config import PINECONE_API_KEY, PINECONE_INDEX


# class PineconeVectorIndex:

#     def __init__(self):

#         print("🌲 Initializing Pinecone Vector Index")

#         self.pc = Pinecone(api_key=PINECONE_API_KEY)

#         self.index = self.pc.Index(PINECONE_INDEX)

#         self.embedder = EmbeddingClient()

#         print("✅ Pinecone index ready")

#     # --------------------------------
#     # Vector Indexing
#     # --------------------------------

#     def index_chunks(self, document, chunks, batch_size=50):

#         if not chunks:
#             print("⚠ No chunks for indexing")
#             return

#         doc_id = document.get("doc_id")

#         metadata = document.get("metadata", {})

#         print(f"🧠 Generating embeddings for {len(chunks)} chunks")

#         embeddings = self.embedder.embed(chunks)

#         vectors = []

#         for chunk, emb in zip(chunks, embeddings):

#             chunk_id = str(uuid.uuid4())

#             vectors.append({
#                 "id": f"{doc_id}_{chunk_id}",
#                 "values": emb,
#                 "metadata": {

#                     "doc_id": doc_id,

#                     "text": chunk,

#                     "topic": metadata.get("topic"),

#                     "keywords": metadata.get("keywords"),

#                     "source": "pdf_ingestion",

#                 }
#             })

#         print(f"📦 Preparing {len(vectors)} vectors")

#         batches = [
#             vectors[i:i + batch_size]
#             for i in range(0, len(vectors), batch_size)
#         ]

#         print(f"🚀 Total batches: {len(batches)}")

#         # --------------------------------
#         # Parallel Upserts
#         # --------------------------------

#         with ThreadPoolExecutor(max_workers=5) as executor:

#             executor.map(self._upsert_batch, batches)

#         print("✅ Pinecone indexing complete")

#     # --------------------------------
#     # Upsert Helper
#     # --------------------------------

#     def _upsert_batch(self, batch):

#         print(f"⬆ Upserting batch of size {len(batch)}")

#         self.index.upsert(vectors=batch)

import uuid
import hashlib
from concurrent.futures import ThreadPoolExecutor

from pinecone import Pinecone
from embedding.embedding_client import EmbeddingClient
from config.config import PINECONE_API_KEY, PINECONE_INDEX


class PineconeVectorIndex:

    def __init__(self):

        print("🌲 Initializing Pinecone Vector Index")

        self.pc = Pinecone(api_key=PINECONE_API_KEY)

        self.index = self.pc.Index(PINECONE_INDEX)

        self.embedder = EmbeddingClient()

        # chunk hash cache
        self.chunk_hashes = set()

        print("✅ Pinecone index ready")

    def _hash_chunk(self, text):

        return hashlib.sha256(text.encode()).hexdigest()

    def index_chunks(self, document, chunks, batch_size=50):

        if not chunks:
            print("⚠ No chunks for indexing")
            return

        doc_id = document["doc_id"]

        metadata = document.get("metadata", {})

        # -------------------------
        # Deduplicate chunks
        # -------------------------

        unique_chunks = []

        for chunk in chunks:

            h = self._hash_chunk(chunk)

            if h in self.chunk_hashes:
                continue

            self.chunk_hashes.add(h)

            unique_chunks.append(chunk)

        print(f"🧹 Deduplicated chunks: {len(unique_chunks)}")

        embeddings = self.embedder.embed(unique_chunks)

        vectors = []

        for chunk, emb in zip(unique_chunks, embeddings):

            chunk_id = str(uuid.uuid4())

            vectors.append({

                "id": f"{doc_id}_{chunk_id}",

                "values": emb,

                "metadata": {

                    "doc_id": doc_id,

                    "text": chunk,

                    "topic": metadata.get("topic"),

                    "keywords": metadata.get("keywords"),

                    "source": "pdf_ingestion"
                }
            })

        batches = [
            vectors[i:i + batch_size]
            for i in range(0, len(vectors), batch_size)
        ]

        print(f"🚀 Upserting {len(batches)} batches")

        with ThreadPoolExecutor(max_workers=5) as executor:

            executor.map(self._upsert_batch, batches)

        print("✅ Pinecone indexing complete")

    def _upsert_batch(self, batch):

        self.index.upsert(vectors=batch)