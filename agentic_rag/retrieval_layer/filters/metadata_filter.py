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

                # # ✅ FIX: handle list filters properly
                # if isinstance(v, list):
                #     if meta.get(k) not in v:
                #         keep = False
                #         break
                if isinstance(v, list):
                    meta_val = str(meta.get(k, "")).lower()
                    if not any(str(val).lower() in meta_val for val in v):
                        keep = False
                        break
                else:
                    if meta.get(k) != v:
                        keep = False
                        break

            if keep:
                results.append(d)

        print("🔹 Metadata Filter Applied:", filters)
        print("🔹 Docs After Filter:", len(results))

        return results