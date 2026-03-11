import re


class SectionDetector:

    HEADINGS = [
        "abstract",
        "introduction",
        "background",
        "method",
        "methods",
        "results",
        "discussion",
        "conclusion",
        "references"
    ]

    def detect(self, text):

        sections = []
        lines = text.split("\n")

        current = {"title": "root", "content": []}

        for line in lines:

            if self.is_heading(line):

                sections.append(current)

                current = {
                    "title": line.strip(),
                    "content": []
                }

            else:

                current["content"].append(line)

        sections.append(current)

        return sections

    def is_heading(self, line):

        line = line.lower().strip()

        if line in self.HEADINGS:
            return True

        if re.match(r"\d+\.\s+[A-Za-z ]+", line):
            return True

        return False