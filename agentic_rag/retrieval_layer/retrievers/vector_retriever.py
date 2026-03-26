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

    def _build_pinecone_filter(self, metadata_filters):

        """
        Convert planner metadata filters into valid Pinecone filter syntax
        """

        if not metadata_filters:
            return None

        pinecone_filter = {}

        for key, value in metadata_filters.items():

            # handle keyword lists
            if isinstance(value, list):

                pinecone_filter[key] = {"$in": value}

            # handle single values
            else:

                pinecone_filter[key] = {"$eq": value}

        return pinecone_filter


    # @traceable(name="vector_retrieval")
    # def search(self, query, top_k, metadata_filters):

    #     print("\n➡ Using VECTOR retriever")

    #     # generate embedding
    #     embedding = self.embedder.embed([query])[0]

    #     # convert filters to Pinecone format
    #     pinecone_filter = self._build_pinecone_filter(metadata_filters)

    #     print("🔹 Pinecone Filter:", pinecone_filter)

    #     results = self.index.query(
    #         vector=embedding,
    #         top_k=top_k,
    #         include_metadata=True,
    #         filter=pinecone_filter
    #     )

    #     docs = []

    #     for match in results["matches"]:

    #         docs.append(
    #             Document(
    #                 content=match["metadata"]["text"],
    #                 score=match["score"],
    #                 meta=match["metadata"]
    #             )
    #         )

    #     return docs
    @traceable(name="vector_retrieval")
    def search(self, query, top_k, metadata_filters):

        print("\n➡ Using VECTOR retriever")

        embedding = self.embedder.embed([query])[0]

        pinecone_filter = self._build_pinecone_filter(metadata_filters)

        print("🔹 Pinecone Filter:", pinecone_filter)

        # ------------------------------
        # FIRST ATTEMPT (WITH FILTER)
        # ------------------------------
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            filter=pinecone_filter
        )

        docs = []

        for match in results["matches"]:
            docs.append(
                Document(
                    content=match["metadata"].get("text", ""),
                    score=match["score"],
                    meta=match["metadata"]
                )
            )

        print(f"📄 Retrieved Docs (with filter): {len(docs)}")

        # ------------------------------
        # ✅ FIX: FALLBACK WITHOUT FILTER
        # ------------------------------
        if len(docs) == 0 and pinecone_filter is not None:

            print("⚠ No results with filter → retry WITHOUT filter")

            results = self.index.query(
                vector=embedding,
                top_k=top_k,
                include_metadata=True
            )

            docs = []

            for match in results["matches"]:
                docs.append(
                    Document(
                        content=match["metadata"].get("text", ""),
                        score=match["score"],
                        meta=match["metadata"]
                    )
                )

            print(f"📄 Retrieved Docs (no filter): {len(docs)}")

        return docs