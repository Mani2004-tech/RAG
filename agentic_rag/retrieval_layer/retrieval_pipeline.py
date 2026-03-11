from langsmith import traceable

from agentic_rag.retrieval_layer.retrievers.vector_retriever import VectorRetriever
from agentic_rag.retrieval_layer.retrievers.bm25_retriever import BM25Retriever
from agentic_rag.retrieval_layer.retrievers.hybrid_retriever import HybridRetriever
from agentic_rag.retrieval_layer.filters.metadata_filter import MetadataFilter
from agentic_rag.retrieval_layer.parent_expansion.parent_expander import ParentExpander
from agentic_rag.retrieval_layer.rerankers.llm_reranker import LLMReranker
from agentic_rag.retrieval_layer.assemblers.cross_encoder_assembler import CrossEncoderAssembler


class RetrievalPipeline:

    def __init__(self):

        self.vector = VectorRetriever()
        self.bm25 = BM25Retriever()

        self.hybrid = HybridRetriever(
            self.vector,
            self.bm25
        )

        self.filter = MetadataFilter()
        self.expander = ParentExpander()
        self.reranker = LLMReranker()
        self.assembler = CrossEncoderAssembler()

    # @traceable(name="retrieval_pipeline")
    # def run(self, query, index, top_k, filters):
    #     print("\n🔹 Retrieval Query:", query)
    #     print("🔹 Index:", index)
    #     if index == "vector":
    #         docs = self.vector.search(query, top_k, filters)

    #     elif index == "bm25":
    #         docs = self.bm25.search(query, top_k)

    #     else:
    #         docs = self.hybrid.search(query, top_k)
    #     print("🔹 Retrieved Docs:", len(docs))
    #     docs = self.filter.apply(docs, filters)

    #     docs = self.expander.expand(docs)

    #     docs = self.reranker.rerank(query, docs)

    #     docs = self.assembler.rerank(query, docs)
    #     print("\n🔹 Final Sources Used:")
    #     print("\n🔹 Final Sources Used:")

    #     for i,d in enumerate(docs[:5]):
    #         print(f"Doc{i+1}:", d.content[:200])
    #     return docs

    @traceable(name="retrieval_pipeline")
    def run(self, query, index, top_k, filters):

        print("\n🔹 Retrieval Query:", query)
        print("🔹 Index:", index)

        if index == "vector":

            docs = self.vector.search(query, top_k, filters)

        elif index == "bm25":

            docs = self.bm25.search(query, top_k)

        else:

            docs = self.hybrid.search(query, top_k, filters)

        print("🔹 Retrieved Docs:", len(docs))

        docs = self.filter.apply(docs, filters)

        docs = self.expander.expand(docs)

        docs = self.reranker.rerank(query, docs)

        docs = self.assembler.rerank(query, docs)

       
        print("\n🔹 Final Sources Used:")

        for i,d in enumerate(docs[:5]):
            print(f"Doc{i+1}:", d.content[:200])

        return docs