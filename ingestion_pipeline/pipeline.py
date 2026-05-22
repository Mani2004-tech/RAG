from chunking.strategy import ChunkingStrategy
from indexing.multi_index_pipeline import MultiIndexPipeline
from monitoring.langsmith_monitor import LangsmithMonitor
from preprocessing_pipeline.deduplicator import DocumentDeduplicator
from preprocessing_pipeline.preprocessing_pipeline import PreprocessingPipeline


class AgenticRAGPipeline:

    def __init__(self):
        print("🚀 Agentic RAG Pipeline Starting")

        self.monitor = LangsmithMonitor()
        self.preprocess = PreprocessingPipeline()
        self.chunker = ChunkingStrategy()
        self.indexing = MultiIndexPipeline()
        self.dedup = DocumentDeduplicator()

    def run(self, pdf_path, strategy="semantic"):
        print("📄 Running ingestion pipeline")

        processed_text, metadata = self.preprocess.run(pdf_path)

        if self.dedup.is_duplicate(processed_text):
            print("⚠ Duplicate document skipped")
            return {"status": "duplicate"}

        self.monitor.trace_preprocessing(processed_text)
        self.monitor.trace_metadata(metadata)
        print("Processed text length:", len(processed_text))

        if strategy == "semantic":
            chunks = self.chunker.run("semantic", metadata["sentences"])

        elif strategy == "token":
            chunks = self.chunker.run("token", processed_text)

        elif strategy == "sliding":
            chunks = self.chunker.run("sliding", processed_text)

        elif strategy == "page":
            chunks = self.chunker.run("page", metadata["sentences"])

        elif strategy == "haystack":
            chunks = self.chunker.run("haystack", metadata["sentences"])

        else:
            raise ValueError("Invalid chunking strategy")

        print("📦 Total chunks:", len(chunks))
        self.monitor.trace_chunking(chunks)

        document = {
            "doc_id": pdf_path,
            "text": processed_text,
            "metadata": metadata,
        }

        index_results = self.indexing.run(document, chunks)
        self.monitor.trace_indexing(index_results)

        print("✅ Document indexed successfully")

        return {
            "chunks": chunks,
            "metadata": metadata,
            "indexes": index_results,
        }
