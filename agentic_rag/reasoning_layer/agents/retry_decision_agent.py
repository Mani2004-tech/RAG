from langsmith import traceable


class RetryDecisionAgent:

    @traceable(name="retry_decision")
    def decide(self, reasoning_result):

        if reasoning_result["needs_retrieval"]:
            return True

        if reasoning_result["confidence"] < 0.6:
            return True

        return False