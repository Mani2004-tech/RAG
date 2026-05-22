import hashlib
import uuid
from concurrent.futures import ThreadPoolExecutor

from pinecone import Pinecone

from config.config import PINECONE_API_KEY, PINECONE_INDEX
from embedding.embedding_client import EmbeddingClient


class PineconeVectorIndex:

    def __init__(self):
        print("🌲 Initializing Pinecone Vector Index")

        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(PINECONE_INDEX)
        self.embedder = EmbeddingClient()
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
                    "source": "pdf_ingestion",
                },
            })

        batches = [
            vectors[i : i + batch_size]
            for i in range(0, len(vectors), batch_size)
        ]

        print(f"🚀 Upserting {len(batches)} batches")

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self._upsert_batch, batches)

        print("✅ Pinecone indexing complete")

    def _upsert_batch(self, batch):
        self.index.upsert(vectors=batch)
