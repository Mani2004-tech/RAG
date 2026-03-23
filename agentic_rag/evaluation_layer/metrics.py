from deepeval.metrics import (

    AnswerRelevancyMetric,

    FaithfulnessMetric

)

from agentic_rag.evaluation_layer.deepeval_model import GroqEvalModel


class EvaluationMetrics:

    def __init__(self):

        model = GroqEvalModel()

        self.answer = AnswerRelevancyMetric(

            model=model,

            threshold=0.5

        )

        self.faith = FaithfulnessMetric(

            model=model,

            threshold=0.5

        )