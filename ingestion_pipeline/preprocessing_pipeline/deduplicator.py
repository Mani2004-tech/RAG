import hashlib

class DocumentDeduplicator:

    def __init__(self):
        self.hash_cache = set()

    def hash_document(self, text: str):

        return hashlib.sha256(text.encode()).hexdigest()

    def is_duplicate(self, text: str):

        h = self.hash_document(text)

        if h in self.hash_cache:
            return True

        self.hash_cache.add(h)
        return False