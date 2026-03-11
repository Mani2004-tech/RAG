class ParentExpander:

    def expand(self, docs):

        expanded = []

        for d in docs:

            parent = d.meta.get("parent_doc")

            if parent:
                expanded.append(parent)

            expanded.append(d)

        return expanded