from indexing.pgsql_store import PgSQLStore


class TemporalIndex:

    def __init__(self):
        print("⏱ Temporal index initialized")
        self.db = PgSQLStore()

    def store_batch(self, records):
        self.db.insert_batch("temporal_index", records)
