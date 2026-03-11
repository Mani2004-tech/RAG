class PageChunker:

    def chunk(self, pages):

        chunks = []

        for page in pages:

            chunks.append({
                "chunk_text": page["text"],
                "page": page["page_number"]
            })

        return chunks