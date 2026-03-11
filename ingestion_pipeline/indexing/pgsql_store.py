# # import psycopg2
# # from config.config import PG_HOST, PG_DB, PG_USER, PG_PASSWORD


# # class PgSQLStore:

# #     def __init__(self):

# #         print("🔌 Connecting to PostgreSQL...")

# #         self.conn = psycopg2.connect(
# #             host=PG_HOST,
# #             database=PG_DB,
# #             user=PG_USER,
# #             password=PG_PASSWORD
# #         )

# #         self.cur = self.conn.cursor()

# #         print("✅ PostgreSQL connected")

# #     def insert_record(self, table, data):

# #         columns = ",".join(data.keys())
# #         values = list(data.values())

# #         placeholders = ",".join(["%s"] * len(values))

# #         query = f"""
# #         INSERT INTO {table} ({columns})
# #         VALUES ({placeholders})
# #         """

# #         print(f"📥 Inserting into {table}")

# #         self.cur.execute(query, values)

# #         self.conn.commit()

# import psycopg2
# from config.config import PG_HOST, PG_DB, PG_USER, PG_PASSWORD


# class PgSQLStore:

#     def __init__(self):

#         print("🔌 Connecting to PostgreSQL...")

#         self.conn = psycopg2.connect(
#             host=PG_HOST,
#             database=PG_DB,
#             user=PG_USER,
#             password=PG_PASSWORD
#         )

#         self.cur = self.conn.cursor()

#         print("✅ PostgreSQL connected")

#         # Ensure tables exist
#         self._ensure_tables()

#     # ----------------------------------------
#     # Create required tables
#     # ----------------------------------------

#     def _ensure_tables(self):

#         print("📦 Ensuring index tables exist")

#         self.cur.execute("""
#         CREATE TABLE IF NOT EXISTS parent_child_index (
#             id SERIAL PRIMARY KEY,
#             parent_id TEXT,
#             chunk_id TEXT,
#             text TEXT
#         );
#         """)

#         self.cur.execute("""
#         CREATE TABLE IF NOT EXISTS temporal_index (
#             id SERIAL PRIMARY KEY,
#             chunk_id TEXT,
#             text TEXT,
#             timestamp TIMESTAMP
#         );
#         """)

#         self.cur.execute("""
#         CREATE TABLE IF NOT EXISTS knowledge_graph (
#             id SERIAL PRIMARY KEY,
#             doc_id TEXT,
#             entity TEXT,
#             type TEXT
#         );
#         """)

#         self.conn.commit()

#         print("✅ Index tables verified")

#     # ----------------------------------------
#     # Insert records
#     # ----------------------------------------

#     def insert_record(self, table, data):

#         columns = ",".join(data.keys())

#         values = list(data.values())

#         placeholders = ",".join(["%s"] * len(values))

#         query = f"""
#         INSERT INTO {table} ({columns})
#         VALUES ({placeholders})
#         """

#         print(f"📥 Inserting into {table}")

#         self.cur.execute(query, values)

#         self.conn.commit()

import psycopg2
from psycopg2.extras import execute_batch
from config.config import PG_HOST, PG_DB, PG_USER, PG_PASSWORD


class PgSQLStore:

    def __init__(self):

        print("🔌 Connecting to PostgreSQL...")

        self.conn = psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )

        self.cur = self.conn.cursor()

        print("✅ PostgreSQL connected")

        self._ensure_tables()

    # ----------------------------
    # Create tables if missing
    # ----------------------------

    def _ensure_tables(self):

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS parent_child_index (
            id SERIAL PRIMARY KEY,
            parent_id TEXT,
            chunk_id TEXT,
            text TEXT
        );
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS temporal_index (
            id SERIAL PRIMARY KEY,
            chunk_id TEXT,
            text TEXT,
            timestamp TIMESTAMP
        );
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_graph (
            id SERIAL PRIMARY KEY,
            doc_id TEXT,
            entity TEXT,
            type TEXT
        );
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS summary_index (
            id SERIAL PRIMARY KEY,
            doc_id TEXT,
            summary TEXT
        );
        """)

        self.conn.commit()

        print("📦 Index tables verified")

    # ----------------------------
    # Single insert
    # ----------------------------

    def insert_record(self, table, data):

        columns = ",".join(data.keys())

        values = list(data.values())

        placeholders = ",".join(["%s"] * len(values))

        query = f"""
        INSERT INTO {table} ({columns})
        VALUES ({placeholders})
        """

        self.cur.execute(query, values)

        self.conn.commit()

    # ----------------------------
    # Batch insert
    # ----------------------------

    def insert_batch(self, table, rows):

        if not rows:
            return

        columns = rows[0].keys()

        column_str = ",".join(columns)

        placeholders = ",".join(["%s"] * len(columns))

        query = f"""
        INSERT INTO {table} ({column_str})
        VALUES ({placeholders})
        """

        values = [tuple(row[col] for col in columns) for row in rows]

        print(f"📦 Batch inserting {len(values)} rows into {table}")

        execute_batch(self.cur, query, values)

        self.conn.commit()