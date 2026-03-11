# from .vector_index_pinecone import PineconeVectorIndex
# from .bm25_index_pgsql import BM25PostgresIndex
# from .hybrid_index import HybridIndexer
# from .parent_child_index import ParentChildIndex
# from .summary_tree_index import SummaryTreeIndex
# from .temporal_index import TemporalIndex
# from .knowledge_graph_index import KnowledgeGraphIndex


# class MultiIndexPipeline:

#     def __init__(self):

#         print("🚀 Initializing Multi Index Pipeline")

#         self.vector = PineconeVectorIndex()

#         self.bm25 = BM25PostgresIndex()

#         self.hybrid = HybridIndexer(self.vector, self.bm25)

#         self.parent_child = ParentChildIndex()

#         self.summary = SummaryTreeIndex()

#         self.temporal = TemporalIndex()

#         self.kg = KnowledgeGraphIndex()

#     # --------------------------------
#     # Main Indexing Pipeline
#     # --------------------------------

#     def run(self, document, chunks):

#         if not chunks:
#             print("⚠ Skipping indexing because no chunks")
#             return {}

#         print("📚 Starting indexing pipeline")

#         doc_id = document.get("doc_id")

#         metadata = document.get("metadata", {})

#         # --------------------------------
#         # Hybrid Index (Vector + BM25)
#         # --------------------------------

#         self.hybrid.index(document, chunks)

#         parent_child_records = []

#         # --------------------------------
#         # Parent Child + Temporal + KG
#         # --------------------------------

#         for i, chunk in enumerate(chunks):

#             chunk_id = f"{doc_id}_chunk_{i}"

#             self.parent_child.store(
#                 parent_id=doc_id,
#                 chunk_id=chunk_id,
#                 text=chunk
#             )

#             self.temporal.store(
#                 chunk_id=chunk_id,
#                 text=chunk
#             )

#             # Knowledge graph extraction

#             entities = self.kg.extract_entities(chunk)

#             self.kg.store_entities(doc_id, entities)

#             parent_child_records.append({
#                 "parent_id": doc_id,
#                 "chunk_id": chunk_id
#             })

#         # --------------------------------
#         # Document Summary
#         # --------------------------------

#         summary = self.summary.generate_summary(
#             " ".join(chunks[:5])
#         )

#         print("✅ Multi indexing complete")

#         return {

#             "doc_id": doc_id,

#             "chunks_indexed": len(chunks),

#             "summary": summary,

#             "parent_child_records": parent_child_records

#         }

from datetime import datetime

from .vector_index_pinecone import PineconeVectorIndex
from .bm25_index_pgsql import BM25PostgresIndex
from .hybrid_index import HybridIndexer
from .parent_child_index import ParentChildIndex
from .summary_tree_index import SummaryTreeIndex
from .temporal_index import TemporalIndex
from .knowledge_graph_index import KnowledgeGraphIndex
from .pgsql_store import PgSQLStore


class MultiIndexPipeline:

    def __init__(self):

        print("🚀 Initializing Multi Index Pipeline")

        self.vector = PineconeVectorIndex()

        self.bm25 = BM25PostgresIndex()

        self.hybrid = HybridIndexer(self.vector, self.bm25)

        self.parent_child = ParentChildIndex()

        self.summary = SummaryTreeIndex()

        self.temporal = TemporalIndex()

        self.kg = KnowledgeGraphIndex()

        # DB for summary storage
        self.db = PgSQLStore()

    # --------------------------------
    # Main Indexing Pipeline
    # --------------------------------

    def run(self, document, chunks):

        if not chunks:
            print("⚠ Skipping indexing because no chunks")
            return {}

        print("📚 Starting indexing pipeline")

        doc_id = document.get("doc_id")

        metadata = document.get("metadata", {})

        # --------------------------------
        # Hybrid Index (Vector + BM25)
        # --------------------------------

        self.hybrid.index(document, chunks)

        # --------------------------------
        # Batch storage structures
        # --------------------------------

        parent_rows = []
        temporal_rows = []
        kg_rows = []

        # --------------------------------
        # Per Chunk Processing
        # --------------------------------

        for i, chunk in enumerate(chunks):

            chunk_id = f"{doc_id}_chunk_{i}"

            # Parent-child
            parent_rows.append({
                "parent_id": doc_id,
                "chunk_id": chunk_id,
                "text": chunk
            })

            # Temporal index
            temporal_rows.append({
                "chunk_id": chunk_id,
                "text": chunk,
                "timestamp": datetime.utcnow()
            })

            # Knowledge graph entities
            entities = self.kg.extract_entities(chunk)

            for e in entities:
                kg_rows.append({
                    "doc_id": doc_id,
                    "entity": e["text"],
                    "type": e["label"]
                })

        # --------------------------------
        # Batch Inserts
        # --------------------------------

        print("📦 Batch inserting parent-child records")
        self.parent_child.db.insert_batch("parent_child_index", parent_rows)

        print("📦 Batch inserting temporal records")
        self.temporal.db.insert_batch("temporal_index", temporal_rows)

        if kg_rows:
            print("📦 Batch inserting knowledge graph entities")
            self.kg.db.insert_batch("knowledge_graph", kg_rows)

        # --------------------------------
        # Document Summary
        # --------------------------------

        summary = self.summary.generate_summary(
            " ".join(chunks[:5])
        )

        # store summary in DB
        self.db.insert_record(
            "summary_index",
            {
                "doc_id": doc_id,
                "summary": summary
            }
        )

        print("✅ Multi indexing complete")

        return {

            "doc_id": doc_id,

            "chunks_indexed": len(chunks),

            "summary": summary,

            "entities_extracted": len(kg_rows)

        }