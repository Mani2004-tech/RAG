import psycopg2
from haystack import Document
from langsmith import traceable

from agentic_rag.config.config import PG_DB, PG_HOST, PG_PASSWORD, PG_USER


class BM25Retriever:

    def __init__(self):
        self.conn = psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD,
        )

    @traceable(name="bm25_retrieval")
    def search(self, query, top_k):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT content
            FROM bm25_index
            ORDER BY ts_rank_cd(
                to_tsvector(content),
                plainto_tsquery(%s)
            ) DESC
            LIMIT %s
            """,
            (query, top_k),
        )
        rows = cur.fetchall()
        return [Document(content=r[0]) for r in rows]
