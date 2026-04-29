from agentic_rag.evaluation_layer.evaluator import Evaluator
from langsmith import traceable


class EvaluationService:

    def __init__(self):
        print("📊 Evaluation Service Ready")
        self.evaluator = Evaluator()

    @traceable(name="evaluation_service")
    def run(self, query, answer, docs):

        if not answer or answer == "NOT_FOUND":
            return {"trusted": False, "reason": "invalid_answer"}

        if not docs:
            return {"trusted": False, "reason": "no_context"}

        # context = []

        # for d in docs[:5]:
        #     if hasattr(d, "content"):
        #         context.append(d.content)
        #     else:
        #         context.append(str(d))
        context = []

        query_terms = query.lower().split()

        for d in docs:
            # content = getattr(d, "content", str(d))
            if hasattr(d, "content"):
                content = d.content
            elif hasattr(d, "page_content"):
                content = d.page_content
            else:
                content = str(d)
            content_lower = content.lower()

            # 🔥 relevance filtering
            if any(term in content_lower for term in query_terms[:2]):
                context.append(content)

        # fallback if nothing matched
        if not context:
            context = [getattr(d, "content", str(d)) for d in docs[:3]]

        scores = self.evaluator.evaluate(query, answer, context)

        # ------------------------------
        # TRUST LOGIC
        # ------------------------------
        scores["trusted"] = True

        if scores.get("answer_relevancy", 0) < 0.5:
            scores["trusted"] = False

        if scores.get("faithfulness", 0) < 0.5:
            scores["trusted"] = False

        if scores.get("contextual_recall", 0) < 0.2:
            scores["trusted"] = False

        if scores.get("toxicity", 0) > 0.5:
            scores["trusted"] = False

        if scores.get("pii_leakage", 0) > 0.3:
            scores["trusted"] = False

        print("\n📊 FULL EVAL:", scores)

        return scores