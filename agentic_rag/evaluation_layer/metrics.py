from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric
)

from agentic_rag.evaluation_layer.deepeval_model import LocalEvalModel


# ------------------------------
# SAFE WRAPPER (FIX DEEPEVAL BUG)
# ------------------------------
class SafeMetricWrapper:
    def __init__(self, metric):
        self.metric = metric
        self.score = 0

    def measure(self, test):
        try:
            self.metric.measure(test)
            self.score = self.metric.score
        except Exception as e:
            print("⚠ DeepEval bug:", e)
            self.score = 0


class EvaluationMetrics:

    def __init__(self):

        model = LocalEvalModel()

        # ✅ THESE WORK FINE (DO NOT WRAP)
        self.answer = AnswerRelevancyMetric(model=model, threshold=0.5)
        self.faith = FaithfulnessMetric(model=model, threshold=0.5)

        # 🔥 THESE NEED WRAPPER (BUG FIX)
        self.context_precision = SafeMetricWrapper(
            ContextualPrecisionMetric(
                model=model,
                threshold=0.5
            )
        )

        self.context_recall = SafeMetricWrapper(
            ContextualRecallMetric(
                model=model,
                threshold=0.5
            )
        )

        self.context_relevancy = SafeMetricWrapper(
            ContextualRelevancyMetric(
                model=model,
                threshold=0.5
            )
        )