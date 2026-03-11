import re


class CitationExtractor:

    def extract(self, text):

        patterns = [
            r"\([A-Za-z]+ et al\., \d{4}\)",
            r"\([A-Za-z]+, \d{4}\)",
            r"\[\d+\]"
        ]

        citations = []

        for p in patterns:

            matches = re.findall(p, text)

            citations.extend(matches)

        return list(set(citations))