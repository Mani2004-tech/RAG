import psycopg2
from haystack import Document
from agentic_rag.config.config import *


class TemporalRetriever:

    def __init__(self):

        self.conn = psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )

    def search(self, query, top_k):

        cur=self.conn.cursor()

        cur.execute(
        """
        SELECT text,timestamp
        FROM temporal_index
        ORDER BY timestamp DESC
        LIMIT %s
        """,
        (top_k,)
        )

        rows=cur.fetchall()

        docs=[]

        for r in rows:

            docs.append(
                Document(
                    content=r[0],
                    meta={"timestamp":str(r[1])}
                )
            )

        return docs