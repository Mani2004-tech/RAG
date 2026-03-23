# from langsmith import traceable
# from agentic_rag.llm.llm_client import LLMClient


# class ValidationAgent:

#     def __init__(self):

#         self.llm = LLMClient()

#     @traceable(name="validation_agent")
#     def validate(self, query, answer, docs):

#         prompt = f"""
# Check if the answer is supported by the documents.

# Query:
# {query}

# Answer:
# {answer}

# Documents:
# {docs}

# Return:
# supported:true/false
# """

#         result = self.llm.generate(prompt)

#         print("\n🔹 Validation Result:", result)

#         return "true" in result.lower()

from langsmith import traceable


class RetryDecisionAgent:


    @traceable(name="retry_decision")
    def decide(self, reasoning_result):

        print("\n🔹 Retry Decision:", reasoning_result)

        if reasoning_result.get("needs_retrieval"):

            print("🔁 Retry because retrieval needed")

            return True


        if reasoning_result.get("confidence", 0.7) < 0.6:

            print("🔁 Retry because confidence low")

            return True


        print("✅ No retry")

        return False