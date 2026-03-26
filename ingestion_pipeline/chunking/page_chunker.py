# class PageChunker:

#     def chunk(self, pages):

#         chunks = []

#         for page in pages:

#             chunks.append({
#                 "chunk_text": page["text"],
#                 "page": page["page_number"]
#             })

#         return chunks
from langsmith import traceable

class PageChunker:

    @traceable(name="page_chunking", run_type="tool")
    def chunk(self, pages):

        chunks = []

        for page in pages:

            chunks.append({
                "chunk_text": page["text"],
                "page": page["page_number"]
            })

        return chunks