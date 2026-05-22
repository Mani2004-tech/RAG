from haystack_pipeline.haystack_pipeline import HaystackProcessor

from .page_chunker import PageChunker
from .semantic_chunker import SemanticChunker
from .sliding_window_chunker import SlidingWindowChunker
from .token_chunker import TokenChunker


class ChunkingStrategy:

    def __init__(self):
        self.semantic = SemanticChunker()
        self.page = PageChunker()
        self.sliding = SlidingWindowChunker()
        self.token = TokenChunker()
        self.haystack = HaystackProcessor()

    def run(self, strategy, data):
        if not data:
            print("⚠ No data for chunking")
            return []

        if strategy == "semantic":
            return self.semantic.chunk(data)

        if strategy == "page":
            return self.page.chunk(data)

        if strategy == "sliding":
            return self.sliding.chunk(data)

        if strategy == "token":
            return self.token.chunk(data)

        if strategy == "haystack":
            return self.haystack.process(data)

        raise ValueError("Invalid chunk strategy")
