import psycopg2

from config.config import PG_DB, PG_HOST, PG_PASSWORD, PG_USER


class BM25PostgresIndex:

    def __init__(self):
        self.conn = psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD,
        )
        self._ensure_table()

    def _ensure_table(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bm25_index (
            id SERIAL PRIMARY KEY,
            content TEXT,
            tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
        );
        """)
        cur.execute("""
        CREATE INDEX IF NOT EXISTS bm25_tsv_idx
        ON bm25_index
        USING GIN(tsv);
        """)
        self.conn.commit()

    def index_chunks(self, chunks):
        if not chunks:
            return

        cur = self.conn.cursor()
        for chunk in chunks:
            cur.execute(
                """
                INSERT INTO bm25_index(content)
                VALUES(%s)
                """,
                (chunk,),
            )
        self.conn.commit()
