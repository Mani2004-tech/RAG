from agentic_rag.evaluation_layer.evaluator import Evaluator


class EvaluationService:

    def __init__(self):

        print("📊 Evaluation Service Ready")

        self.evaluator=Evaluator()

    


    def run(self,query,answer,docs):

        context=[d.content for d in docs[:5]]


        scores=self.evaluator.evaluate(

            query,

            answer,

            context

        )


        print("\n📊 DeepEval Scores:")

        print(scores)


        # FINAL QUALITY DECISION

        scores["trusted"]=True


        if scores["faithfulness"]<0.6:

            scores["trusted"]=False


        if scores["answer_relevancy"]<0.6:

            scores["trusted"]=False


        return scores