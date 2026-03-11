import psycopg2
from agentic_rag.config.config import *


class MemoryStore:

    def __init__(self):

        self.conn = psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )

    def store_query(self, query, decision):

        cur = self.conn.cursor()

        cur.execute(
        """
        INSERT INTO rag_memory(query, decision)
        VALUES(%s,%s)
        """,
        (query, str(decision))
        )

        self.conn.commit()

    def store_failure(self, query, reason):

        cur = self.conn.cursor()

        cur.execute(
        """
        INSERT INTO rag_failures(query, reason)
        VALUES(%s,%s)
        """,
        (query, reason)
        )

        self.conn.commit()

    def fetch_similar_queries(self, query):

        cur = self.conn.cursor()

        cur.execute(
        """
        SELECT query, decision
        FROM rag_memory
        ORDER BY similarity(query,%s) DESC
        LIMIT 5
        """,
        (query,)
        )

        return cur.fetchall()