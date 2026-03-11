import re


class HierarchyBuilder:

    def build(self, sections):

        tree = []

        for sec in sections:

            level = self.get_level(sec["title"])

            node = {
                "title": sec["title"],
                "level": level,
                "content": sec["content"]
            }

            tree.append(node)

        return tree

    def get_level(self, title):

        match = re.match(r"(\d+(\.\d+)*)", title)

        if match:

            return match.group(1).count(".") + 1

        return 1