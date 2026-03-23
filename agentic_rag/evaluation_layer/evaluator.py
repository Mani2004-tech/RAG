from deepeval.test_case import LLMTestCase

from agentic_rag.evaluation_layer.metrics import EvaluationMetrics


class Evaluator:

    def __init__(self):

        self.metrics = EvaluationMetrics()


    def evaluate(self, query, answer, context):

        test = LLMTestCase(

            input=query,

            actual_output=answer,

            expected_output=answer,

            retrieval_context=context

        )


        self.metrics.answer.measure(test)

        self.metrics.faith.measure(test)


        return {

            "answer_relevancy":

            self.metrics.answer.score,

            "faithfulness":

            self.metrics.faith.score

        }