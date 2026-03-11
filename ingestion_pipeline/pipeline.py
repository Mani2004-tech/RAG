# from preprocessing_pipeline.preprocessing_pipeline import PreprocessingPipeline
# from chunking.strategy import ChunkingStrategy
# from indexing.multi_index_pipeline import MultiIndexPipeline
# from monitoring.langsmith_monitor import LangsmithMonitor


# class AgenticRAGPipeline:

    

#     def __init__(self):

#         self.monitor = LangsmithMonitor()

#         # preprocessing layer
#         self.preprocess = PreprocessingPipeline()

#         # chunking layer
#         self.chunker = ChunkingStrategy()

#         # indexing layer
#         self.indexing = MultiIndexPipeline()

#     def run(self, pdf_path, strategy="semantic"):

#         # -------------------------------
#         # PREPROCESSING
#         # -------------------------------

#         processed_text, metadata = self.preprocess.run(pdf_path)

#         self.monitor.trace_preprocessing(processed_text)

#         self.monitor.trace_metadata(metadata)

#         print("Processed text length:", len(processed_text))
#         print("Sentence count:", len(metadata["sentences"]))

#         # -------------------------------
#         # CHUNKING
#         # -------------------------------
#         MAX_CHUNK_LENGTH = 2000

    
#         chunks = self.chunker.run("semantic", metadata["sentences"])
#         chunks = [c[:MAX_CHUNK_LENGTH] for c in chunks]
        
#         if strategy == "semantic":

#             chunks = self.chunker.run(
#                 "semantic",
#                 metadata["sentences"]
#             )

#         elif strategy == "sliding":

#             chunks = self.chunker.run(
#                 "sliding",
#                 processed_text
#             )

#         elif strategy == "token":

#             chunks = self.chunker.run(
#                 "token",
#                 processed_text
#             )

#         elif strategy == "page":

#             chunks = self.chunker.run(
#                 "page",
#                 processed_text
#             )

#         else:

#             raise ValueError("Invalid chunking strategy")

#         self.monitor.trace_chunking(chunks)

#         # -------------------------------
#         # DOCUMENT OBJECT
#         # -------------------------------

#         document = {

#             "doc_id": pdf_path,
#             "text": processed_text,
#             "metadata": metadata

#         }

#         # -------------------------------
#         # MULTI INDEXING
#         # -------------------------------

#         index_results = self.indexing.run(
#             document,
#             chunks
#         )

#         self.monitor.trace_indexing(index_results)

#         return {

#             "chunks": chunks,
#             "metadata": metadata,
#             "indexes": index_results

#         }


# if __name__ == "__main__":

#     pipeline = AgenticRAGPipeline()

#     result = pipeline.run(
#         r"C:\Agentic_RAG\Agentic_RAG\ingestion_pipeline\test.pdf",
#         strategy="semantic"
#     )

#     print("Chunks:", result["chunks"][:3])
#     print("Metadata:", result["metadata"])

# from preprocessing_pipeline.preprocessing_pipeline import PreprocessingPipeline
# from chunking.strategy import ChunkingStrategy
# from indexing.multi_index_pipeline import MultiIndexPipeline
# from monitoring.langsmith_monitor import LangsmithMonitor
# from preprocessing_pipeline.deduplicator import DocumentDeduplicator


# class AgenticRAGPipeline:

#     def __init__(self):

#         print("🚀 Agentic RAG Ingestion Pipeline")

#         self.monitor = LangsmithMonitor()

#         self.preprocess = PreprocessingPipeline()

#         self.chunker = ChunkingStrategy()

#         self.indexing = MultiIndexPipeline()

#         self.dedup = DocumentDeduplicator()

#     def run(self, pdf_path, strategy="semantic"):

#         print("📄 Processing:", pdf_path)

#         processed_text, metadata = self.preprocess.run(pdf_path)

#         if self.dedup.is_duplicate(processed_text):

#             print("⚠ Duplicate document skipped")

#             return {"status": "duplicate"}

#         self.monitor.trace_preprocessing(processed_text)

#         self.monitor.trace_metadata(metadata)

#         print("Processed text length:", len(processed_text))

#         print("Sentence count:", len(metadata["sentences"]))

#         # -------------------------------
#         # CHUNKING
#         # -------------------------------

#         if strategy == "semantic":

#             chunks = self.chunker.run(
#                 "semantic",
#                 metadata["sentences"]
#             )

#         elif strategy == "haystack":

#             chunks = self.chunker.run(
#                 "haystack",
#                 metadata["sentences"]
#             )

#         elif strategy == "sliding":

#             chunks = self.chunker.run(
#                 "sliding",
#                 processed_text
#             )

#         elif strategy == "token":

#             chunks = self.chunker.run(
#                 "token",
#                 processed_text
#             )

#         elif strategy == "page":

#             chunks = self.chunker.run(
#                 "page",
#                 metadata["sentences"]
#             )

#         else:

#             raise ValueError("Invalid chunking strategy")

#         print("📦 Total chunks:", len(chunks))

#         self.monitor.trace_chunking(chunks)

#         document = {

#             "doc_id": pdf_path,
#             "text": processed_text,
#             "metadata": metadata

#         }

#         # -------------------------------
#         # INDEXING
#         # -------------------------------

#         index_results = self.indexing.run(
#             document,
#             chunks
#         )

#         self.monitor.trace_indexing(index_results)

#         print("✅ Document indexed successfully")

#         return {

#             "chunks": chunks,
#             "metadata": metadata,
#             "indexes": index_results

#         }
from preprocessing_pipeline.preprocessing_pipeline import PreprocessingPipeline
from chunking.strategy import ChunkingStrategy
from indexing.multi_index_pipeline import MultiIndexPipeline
from monitoring.langsmith_monitor import LangsmithMonitor
from preprocessing_pipeline.deduplicator import DocumentDeduplicator


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

        # -----------------------------
        # Deduplication
        # -----------------------------

        if self.dedup.is_duplicate(processed_text):

            print("⚠ Duplicate document skipped")

            return {"status": "duplicate"}

        self.monitor.trace_preprocessing(processed_text)

        self.monitor.trace_metadata(metadata)

        print("Processed text length:", len(processed_text))

        # -----------------------------
        # Chunking
        # -----------------------------

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

        # -----------------------------
        # Document Object
        # -----------------------------

        document = {

            "doc_id": pdf_path,
            "text": processed_text,
            "metadata": metadata

        }

        # -----------------------------
        # Indexing
        # -----------------------------

        index_results = self.indexing.run(document, chunks)

        self.monitor.trace_indexing(index_results)

        print("✅ Document indexed successfully")

        return {

            "chunks": chunks,
            "metadata": metadata,
            "indexes": index_results

        }