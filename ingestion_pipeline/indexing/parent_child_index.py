# from indexing.pgsql_store import PgSQLStore


# class ParentChildIndex:

#     def __init__(self):

#         print("🌳 Parent-Child index initialized")

#         self.db = PgSQLStore()

#     def store(self, parent_id, chunk_id, text):

#         print("📎 Linking parent-child")

#         self.db.insert_record(
#             "parent_child_index",
#             {
#                 "parent_id": parent_id,
#                 "chunk_id": chunk_id,
#                 "text": text
#             }
#         )
from indexing.pgsql_store import PgSQLStore


class ParentChildIndex:

    def __init__(self):

        print("🌳 Parent-Child index initialized")

        self.db = PgSQLStore()

    def store_batch(self, records):

        self.db.insert_batch("parent_child_index", records)