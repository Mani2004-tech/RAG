
# from langsmith import traceable


# class RetryDecisionAgent:

#     @traceable(name="retry_decision")
#     def decide(self, reasoning_result):

#         print("\n🔹 Retry Decision Input:", reasoning_result)

#         # ✅ CRITICAL FIX
#         if not reasoning_result.get("complete", False):
#             print("🔁 Retry because incomplete answer")
#             return True

#         if reasoning_result.get("needs_retrieval"):
#             print("🔁 Retry because retrieval needed")
#             return True

#         if reasoning_result.get("confidence", 0.7) < 0.6:
#             print("🔁 Retry because low confidence")
#             return True

#         print("✅ No retry needed")

#         return False

from langsmith import traceable


class RetryDecisionAgent:

    @traceable(name="retry_decision")
    def decide(self, reasoning_result):


        print("\n🔹 Retry Decision Input:", reasoning_result)

        # ✅ FIX: allow confident answers to pass
        if not reasoning_result.get("complete", False):

            # if reasoning_result.get("confidence", 0.0) >= 0.6:
            #     print("⚠ Incomplete but confident → accept")
            #     return False

            print("🔁 Retry because incomplete answer")
            return True

        if reasoning_result.get("needs_retrieval"):
            print("🔁 Retry because retrieval needed")
            return True

        if reasoning_result.get("confidence", 0.7) < 0.6:
            print("🔁 Retry because low confidence")
            return True

        print("✅ No retry needed")
      
        return False