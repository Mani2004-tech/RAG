# from datetime import datetime
# from indexing.pgsql_store import PgSQLStore


# class TemporalIndex:

#     def __init__(self):

#         print("⏱ Temporal index initialized")

#         self.db = PgSQLStore()

#     def store(self, chunk_id, text):

#         print("🕒 Storing temporal record")

#         self.db.insert_record(
#             "temporal_index",
#             {
#                 "chunk_id": chunk_id,
#                 "text": text,
#                 "timestamp": datetime.utcnow()
#             }
#         )

from indexing.pgsql_store import PgSQLStore


class TemporalIndex:

    def __init__(self):

        print("⏱ Temporal index initialized")

        self.db = PgSQLStore()

    def store_batch(self, records):

        self.db.insert_batch("temporal_index", records)