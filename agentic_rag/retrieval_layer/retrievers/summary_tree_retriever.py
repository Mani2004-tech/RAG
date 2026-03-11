import psycopg2
from haystack import Document
from agentic_rag.config.config import *


class SummaryTreeRetriever:

    def __init__(self):

        self.conn=psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )

    def search(self, query, top_k):

        cur=self.conn.cursor()

        cur.execute(
        """
        SELECT summary
        FROM summary_index
        ORDER BY similarity(summary,%s) DESC
        LIMIT %s
        """,
        (query,top_k)
        )

        rows=cur.fetchall()

        return [Document(content=r[0]) for r in rows]