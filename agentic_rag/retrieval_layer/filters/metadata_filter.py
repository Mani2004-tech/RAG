class MetadataFilter:

    def apply(self, docs, filters):

        if not filters:
            return docs

        results = []

        for d in docs:

            meta = getattr(d, "meta", {})

            keep = True

            for k, v in filters.items():

                if k not in meta:
                    continue

                if meta.get(k) != v:
                    keep = False
                    break

            if keep:
                results.append(d)

        print("🔹 Metadata Filter Applied:", filters)
        print("🔹 Docs After Filter:", len(results))

        return results