from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


class PIIDetector:

    def __init__(self):

        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def detect(self, text):

        results = self.analyzer.analyze(
            text=text,
            language="en"
        )

        anonymized = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )

        pii_entities = []

        for r in results:

            pii_entities.append({
                "entity": r.entity_type,
                "score": r.score
            })

        return anonymized.text, pii_entities