# class TokenChunker:

#     def __init__(self, chunk_size=300):

#         self.chunk_size = chunk_size

#     def chunk(self, text):

#         words = text.split()

#         chunks = []

#         for i in range(0, len(words), self.chunk_size):

#             chunk = words[i:i+self.chunk_size]

#             chunks.append(" ".join(chunk))

#         return chunks
from langsmith import traceable

class TokenChunker:

    def __init__(self, chunk_size=300):

        self.chunk_size = chunk_size

    @traceable(name="token_chunking", run_type="tool")
    def chunk(self, text):

        words = text.split()

        chunks = []

        for i in range(0, len(words), self.chunk_size):

            chunk = words[i:i+self.chunk_size]

            chunks.append(" ".join(chunk))

        return chunks