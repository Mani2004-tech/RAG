from langsmith import traceable

from agentic_rag.retrieval_layer.assemblers.cross_encoder_assembler import CrossEncoderAssembler
from agentic_rag.retrieval_layer.filters.metadata_filter import MetadataFilter
from agentic_rag.retrieval_layer.parent_expansion.parent_expander import ParentExpander
from agentic_rag.retrieval_layer.rerankers.llm_reranker import LLMReranker
from agentic_rag.retrieval_layer.retrievers.bm25_retriever import BM25Retriever
from agentic_rag.retrieval_layer.retrievers.hybrid_retriever import HybridRetriever
from agentic_rag.retrieval_layer.retrievers.knowledge_graph_retriver import KnowledgeGraphRetriever
from agentic_rag.retrieval_layer.retrievers.parent_child_retriever import ParentChildRetriever
from agentic_rag.retrieval_layer.retrievers.summary_tree_retriever import SummaryTreeRetriever
from agentic_rag.retrieval_layer.retrievers.temporal_retriever import TemporalRetriever
from agentic_rag.retrieval_layer.retrievers.vector_retriever import VectorRetriever


class RetrievalPipeline:

    def __init__(self):
        print("🚀 Initializing Retrieval Pipeline")

        self.vector = VectorRetriever()
        self.bm25 = BM25Retriever()
        self.hybrid = HybridRetriever(self.vector, self.bm25)

        self.parent = ParentChildRetriever()
        self.temporal = TemporalRetriever()
        self.summary = SummaryTreeRetriever()
        self.kg = KnowledgeGraphRetriever()

        self.filter = MetadataFilter()
        self.expander = ParentExpander()
        self.reranker = LLMReranker()
        self.assembler = CrossEncoderAssembler()

    @traceable(name="retrieval_pipeline")
    def run(self, query, index, top_k, filters):
        print("\n==============================")
        print("🔍 RETRIEVAL PIPELINE START")
        print("Query:", query)
        print("Index:", index)
        print("Top K:", top_k)
        print("==============================")

        if index == "vector":
            print("➡ Using VECTOR retriever")
            docs = self.vector.search(query, top_k, filters)

        elif index == "bm25":
            print("➡ Using BM25 retriever")
            docs = self.bm25.search(query, top_k)

        elif index == "hybrid":
            print("➡ Using HYBRID retriever")
            docs = self.hybrid.search(query, top_k, filters)

        elif index == "parent_child":
            print("➡ Using PARENT CHILD retriever")
            docs = self.parent.search(query, top_k)

        elif index == "temporal":
            print("➡ Using TEMPORAL retriever")
            docs = self.temporal.search(query, top_k)

        elif index == "summary_tree":
            print("➡ Using SUMMARY TREE retriever")
            docs = self.summary.search(query, top_k)

        elif index == "knowledge_graph":
            print("➡ Using KNOWLEDGE GRAPH retriever")
            docs = self.kg.search(query, top_k)

        else:
            print("⚠ Unknown index — fallback HYBRID")
            docs = self.hybrid.search(query, top_k, filters)

        print("📄 Retrieved Docs:", len(docs))

        docs = self.filter.apply(docs, filters)
        docs = self.expander.expand(docs)
        docs = self.reranker.rerank(query, docs)
        docs = self.assembler.rerank(query, docs)

        print("\n📚 FINAL SOURCES")
        for i, d in enumerate(docs[:5]):
            print(f"Doc{i+1}:", d.content[:200])

        print("🔍 RETRIEVAL PIPELINE END\n")
        return docs
