# import requests
# from langsmith import traceable
# from agentic_rag.config.config import LLM_ENDPOINT, MODEL_NAME


# class LLMClient:

#     @traceable(name="llm_call")
#     def generate(self, prompt):

#         payload = {
#             "model": MODEL_NAME,
#             "prompt": prompt,
#             "stream": False
#         }

#         r = requests.post(
#             LLM_ENDPOINT,
#             json=payload
#         )

#         return r.json()["response"]

import requests
from langsmith import traceable
from agentic_rag.config.config import LLM_ENDPOINT, MODEL_NAME


class LLMClient:

    @traceable(name="llm_call")
    def generate(self, prompt):

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        r = requests.post(
            LLM_ENDPOINT,
            json=payload
        )

        try:
            data = r.json()

            # 🔍 DEBUG (IMPORTANT)
            print("🔍 LLM RAW:", data)

            # ✅ OPENAI FORMAT
            if "choices" in data:
                return data["choices"][0]["message"]["content"]

            # ❌ ERROR CASE
            if "error" in data:
                print("❌ LLM ERROR:", data["error"])
                return "ERROR"

            return str(data)

        except Exception as e:
            print("❌ PARSE ERROR:", e)
            return "ERROR"