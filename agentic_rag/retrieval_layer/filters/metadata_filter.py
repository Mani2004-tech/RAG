class MetadataFilter:

    def apply(self, docs, filters):

        if not filters:
            return docs

        results = []

        for d in docs:

            keep = True

            for k, v in filters.items():

                # only filter if metadata key exists
                if k in d.meta:

                    if d.meta.get(k) != v:
                        keep = False
                        break

            if keep:
                results.append(d)

        return results