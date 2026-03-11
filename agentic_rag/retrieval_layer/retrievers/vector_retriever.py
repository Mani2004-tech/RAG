from langsmith import traceable
from haystack import Document
from pinecone import Pinecone
from agentic_rag.embedding.embedding_client import EmbeddingClient
from agentic_rag.config.config import *


class VectorRetriever:

    def __init__(self):

        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(PINECONE_INDEX)

        self.embedder = EmbeddingClient()

    @traceable(name="vector_retrieval")
    def search(self, query, top_k, metadata_filters):

        embedding = self.embedder.embed([query])[0]

        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            filter=metadata_filters
        )

        docs = []

        for match in results["matches"]:

            docs.append(
                Document(
                    content=match["metadata"]["text"],
                    score=match["score"],
                    meta=match["metadata"]
                )
            )

        return docs