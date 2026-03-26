# from typing import List


# class EmbeddingBatcher:

#     def __init__(self, batch_size=100):
#         self.batch_size = batch_size

#     def create_batches(self, texts: List[str]):

#         batches = []

#         for i in range(0, len(texts), self.batch_size):

#             batches.append(texts[i:i+self.batch_size])

#         return batches
from langsmith import traceable
from typing import List


class EmbeddingBatcher:

    def __init__(self, batch_size=100):
        self.batch_size = batch_size

    @traceable(name="embedding_batch_creation", run_type="tool")
    def create_batches(self, texts: List[str]):

        batches = []

        for i in range(0, len(texts), self.batch_size):

            batches.append(texts[i:i+self.batch_size])

        return batches