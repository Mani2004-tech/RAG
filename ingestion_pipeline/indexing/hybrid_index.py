# class HybridIndexer:

#     def __init__(self, vector, bm25):

#         self.vector = vector
#         self.bm25 = bm25

#     def index(self, chunks):

#         if not chunks:
#             print("⚠ No chunks to index")
#             return

#         self.vector.index_chunks(chunks)

#         self.bm25.index_chunks(chunks)

class HybridIndexer:

    def __init__(self, vector, bm25):

        self.vector = vector
        self.bm25 = bm25

        print("⚡ Hybrid index initialized")

    def index(self, document, chunks):

        if not chunks:
            print("⚠ No chunks to index")
            return

        print("🔹 Running Hybrid Indexing")

        print("➡ Vector indexing")
        self.vector.index_chunks(document, chunks)

        print("➡ BM25 indexing")
        self.bm25.index_chunks(chunks)

        print("✅ Hybrid indexing finished")