from indexing.pgsql_store import PgSQLStore


class ParentChildIndex:

    def __init__(self):
        print("🌳 Parent-Child index initialized")
        self.db = PgSQLStore()

    def store_batch(self, records):
        self.db.insert_batch("parent_child_index", records)
