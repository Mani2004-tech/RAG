import spacy


class NLPProcessor:

    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm")

    def process(self, text):

        doc = self.nlp(text)

        tokens = []
        entities = []
        noun_phrases = []
        sentences = []

        for token in doc:

            if token.is_stop:
                continue

            if token.is_punct:
                continue

            if token.pos_ not in ["NOUN", "PROPN", "VERB", "ADJ"]:
                continue

            tokens.append(token.lemma_.lower())

        for ent in doc.ents:

            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

        for chunk in doc.noun_chunks:

            noun_phrases.append(chunk.text)

        for sent in doc.sents:

            sentences.append(sent.text.strip())

        return {
            "processed_text": " ".join(tokens),
            "entities": entities,
            "noun_phrases": noun_phrases,
            "sentences": sentences
        }