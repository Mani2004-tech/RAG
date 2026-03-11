import os
from config.config import LANGCHAIN_API_KEY, LANGCHAIN_PROJECT


class LangsmithMonitor:

    def __init__(self):

        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT

        print("📊 LangSmith monitoring enabled")

    def trace_preprocessing(self, text):

        print("🔎 Preprocessing trace length:", len(text))

    def trace_metadata(self, metadata):

        print("📑 Metadata trace keys:", list(metadata.keys()))

    def trace_chunking(self, chunks):

        print("📦 Chunk trace:", len(chunks))

    def trace_indexing(self, results):

        print("📚 Indexing trace:", results)