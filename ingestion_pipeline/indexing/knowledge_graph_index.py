# import spacy
# from indexing.pgsql_store import PgSQLStore

# nlp = spacy.load("en_core_web_sm")


# class KnowledgeGraphIndex:

#     def __init__(self):

#         print("🧠 Knowledge Graph Index initialized")

#         self.db = PgSQLStore()

#     def extract_entities(self, text):

#         doc = nlp(text)

#         entities = []

#         for ent in doc.ents:

#             entities.append({
#                 "text": ent.text,
#                 "label": ent.label_
#             })

#         print(f"🔎 Extracted {len(entities)} entities")

#         return entities

   
#     def store_entities(self, doc_id, entities):

#         rows = []

#         for e in entities:

#             rows.append({
#                 "doc_id": doc_id,
#                 "entity": e["text"],
#                 "type": e["label"]
#             })

#         self.db.insert_batch("knowledge_graph", rows)
from langsmith import traceable
import spacy
from indexing.pgsql_store import PgSQLStore

nlp = spacy.load("en_core_web_sm")


class KnowledgeGraphIndex:

    def __init__(self):

        print("🧠 Knowledge Graph Index initialized")

        self.db = PgSQLStore()

    @traceable(name="kg_entity_extraction", run_type="tool")
    def extract_entities(self, text):

        doc = nlp(text)

        entities = []

        for ent in doc.ents:

            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

        print(f"🔎 Extracted {len(entities)} entities")

        return entities