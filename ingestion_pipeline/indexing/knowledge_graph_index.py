import spacy

from indexing.pgsql_store import PgSQLStore

nlp = spacy.load("en_core_web_sm")


class KnowledgeGraphIndex:

    def __init__(self):
        print("🧠 Knowledge Graph Index initialized")
        self.db = PgSQLStore()

    def extract_entities(self, text):
        doc = nlp(text)
        entities = [
            {"text": ent.text, "label": ent.label_}
            for ent in doc.ents
        ]
        print(f"🔎 Extracted {len(entities)} entities")
        return entities

    def store_entities(self, doc_id, entities):
        rows = [
            {
                "doc_id": doc_id,
                "entity": e["text"],
                "type": e["label"],
            }
            for e in entities
        ]
        self.db.insert_batch("knowledge_graph", rows)
