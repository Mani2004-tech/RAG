from collections import defaultdict

from langsmith import traceable


class HybridRetriever:

    def __init__(self, vector, bm25):
        self.vector = vector
        self.bm25 = bm25

    @traceable(name="hybrid_retrieval")
    def search(self, query, top_k, metadata_filters=None):
        print("\n🔹 Hybrid Retriever (RRF)")

        vector_docs = self.vector.search(query, top_k, metadata_filters)
        bm25_docs = self.bm25.search(query, top_k)

        print("Vector Docs:", len(vector_docs))
        print("BM25 Docs:", len(bm25_docs))

        k = 60
        scores = defaultdict(float)
        doc_map = {}

        for rank, doc in enumerate(vector_docs):
            doc_id = doc.id
            scores[doc_id] += 1 / (k + rank + 1)
            doc_map[doc_id] = doc

        for rank, doc in enumerate(bm25_docs):
            doc_id = doc.id
            scores[doc_id] += 1 / (k + rank + 1)
            doc_map[doc_id] = doc

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        fused_docs = [doc_map[d[0]] for d in ranked]

        print("🔹 RRF Combined Docs:", len(fused_docs))
        return fused_docs[:top_k]
