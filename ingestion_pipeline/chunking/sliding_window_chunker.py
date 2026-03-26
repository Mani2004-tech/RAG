# class SlidingWindowChunker:

#     def __init__(self, window_size=200, overlap=50):

#         self.window_size = window_size
#         self.overlap = overlap

#     def chunk(self, text):

#         words = text.split()

#         chunks = []

#         start = 0

#         while start < len(words):

#             end = start + self.window_size

#             chunk_words = words[start:end]

#             chunk = " ".join(chunk_words)

#             chunks.append(chunk)

#             start += self.window_size - self.overlap

#         return chunks
from langsmith import traceable

class SlidingWindowChunker:

    def __init__(self, window_size=200, overlap=50):

        self.window_size = window_size
        self.overlap = overlap

    @traceable(name="sliding_window_chunking", run_type="tool")
    def chunk(self, text):

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + self.window_size

            chunk_words = words[start:end]

            chunk = " ".join(chunk_words)

            chunks.append(chunk)

            start += self.window_size - self.overlap

        return chunks