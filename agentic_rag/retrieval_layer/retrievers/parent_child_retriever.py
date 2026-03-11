import psycopg2
from haystack import Document
from agentic_rag.config.config import *


class ParentChildRetriever:

    def __init__(self):

        self.conn = psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )

    def search(self, query, top_k):

        cur = self.conn.cursor()

        cur.execute(
        """
        SELECT parent_id,text
        FROM parent_child_index
        ORDER BY similarity(text,%s) DESC
        LIMIT %s
        """,
        (query,top_k)
        )

        rows = cur.fetchall()

        docs=[]

        for r in rows:

            docs.append(
                Document(
                    id=r[0],
                    content=r[1]
                )
            )

        return docs