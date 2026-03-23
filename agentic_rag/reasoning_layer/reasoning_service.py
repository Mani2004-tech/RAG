from agentic_rag.reasoning_layer.agents.reasoning_agent import ReasoningAgent

from agentic_rag.reasoning_layer.agents.validation_agent import ValidationAgent

from agentic_rag.reasoning_layer.agents.retry_decision_agent import RetryDecisionAgent

from agentic_rag.evaluation_layer.evaluation_service import EvaluationService


class ReasoningService:


    def __init__(self):

        print("🧠 Reasoning Service Started")

        self.reasoning=ReasoningAgent()

        self.validation=ValidationAgent()

        self.retry=RetryDecisionAgent()

        self.evaluation=EvaluationService()


    def run(self,query,answer,docs):

        print("\nSTEP 1 → Reasoning")

        reasoning_result=self.reasoning.evaluate(

            query,

            answer,

            docs

        )


        print("\nSTEP 2 → Validation")

        validation_result=self.validation.validate(

            query,

            answer,

            docs

        )


        print("\nSTEP 3 → Retry Decision")

        retry_needed=self.retry.decide(

            reasoning_result

        )


        if retry_needed:

            print("🔁 Retry Required")

            return{

                "retry":True,

                "reason":"low confidence"

            }


        print("\nSTEP 4 → DeepEval")

        eval_scores=self.evaluation.run(

            query,

            answer,

            docs

        )


        # FINAL GUARDRAIL DECISION

        if not eval_scores["trusted"]:

            print("⚠️ Answer not trusted")

            return{

                "retry":True,

                "reason":"evaluation failed"

            }


        print("\n✅ FINAL ANSWER ACCEPTED")


        return{

            "retry":False,

            "reasoning":reasoning_result,

            "validation":validation_result,

            "evaluation":eval_scores,

            "final_answer":answer

        }