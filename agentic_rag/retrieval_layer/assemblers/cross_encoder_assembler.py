from langsmith import traceable
from sentence_transformers import CrossEncoder


class CrossEncoderAssembler:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    @traceable(name="cross_encoder_rerank")
    def rerank(self, query, docs):

        if not docs:
            return docs
        # ✅ LIMIT for performance
        docs = docs[:5]
        pairs = [[query, d.content] for d in docs]

        scores = self.model.predict(pairs)

        ranked = list(zip(scores, docs))

        # sort by score only
        ranked.sort(key=lambda x: x[0], reverse=True)
   
        return [doc for _, doc in ranked]