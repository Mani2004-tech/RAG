from langsmith import traceable


class RetryDecisionAgent:

    @traceable(name="retry_decision")
    def decide(self, reasoning_result):
        print("\n🔹 Retry Decision Input:", reasoning_result)

        if reasoning_result.get("needs_retrieval"):
            print("🔁 Retry because retrieval needed")
            return True

        if reasoning_result.get("confidence", 0.7) < 0.6:
            print("🔁 Retry because confidence low")
            return True

        print("✅ No retry needed")
        return False
