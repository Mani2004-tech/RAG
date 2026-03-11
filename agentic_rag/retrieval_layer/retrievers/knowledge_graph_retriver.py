import psycopg2
from haystack import Document
from agentic_rag.config.config import *


class KnowledgeGraphRetriever:

    def __init__(self):

        self.conn=psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )

    def search(self, entity, top_k):

        cur=self.conn.cursor()

        cur.execute(
        """
        SELECT doc_id,entity
        FROM knowledge_graph
        WHERE entity=%s
        LIMIT %s
        """,
        (entity,top_k)
        )

        rows=cur.fetchall()

        docs=[]

        for r in rows:

            docs.append(
                Document(
                    id=r[0],
                    content=r[1]
                )
            )

        return docs