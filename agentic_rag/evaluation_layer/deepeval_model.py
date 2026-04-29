# # # import requests
# # # from deepeval.models.base_model import DeepEvalBaseLLM
# # # from types import SimpleNamespace

# # # LLM_ENDPOINT = "http://10.41.134.30:8001/v1/chat/completions"
# # # MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"


# # # class LocalEvalModel(DeepEvalBaseLLM):

# # #     def __init__(self):
# # #         pass

# # #     def load_model(self):
# # #         return None

# # #     # def generate(self, prompt, schema=None, **kwargs):

# # #     #     try:
# # #     #         response = requests.post(
# # #     #             LLM_ENDPOINT,
# # #     #             json={
# # #     #                 "model": MODEL_NAME,
# # #     #                 "prompt": prompt,
# # #     #                 "stream": False
# # #     #             },
# # #     #             timeout=60
# # #     #         )

# # #     #         response.raise_for_status()
# # #     #         text = response.json().get("response", "").strip()

# # #     #     except Exception as e:
# # #     #         print("❌ LLM API Error:", e)
# # #     #         text = ""

# # #     #     if schema:
# # #     #         try:
# # #     #             return schema.model_validate_json(text)
# # #     #         except:
# # #     #             return schema.model_construct()

# # #     #     return text

# # #     def generate(self, prompt, schema=None, **kwargs):

# # #         try:
# # #             response = requests.post(
# # #                 LLM_ENDPOINT,
# # #                 json={
# # #                     "model": MODEL_NAME,
# # #                     "messages": [
# # #                         {"role": "user", "content": prompt}
# # #                     ]
# # #                 },
# # #                 timeout=60
# # #             )

# # #             data = response.json()

# # #             print("🔍 EVAL LLM RAW:", data)

# # #             text = data["choices"][0]["message"]["content"].strip()

# # #         except Exception as e:
# # #             print("❌ LLM API Error:", e)
# # #             text = ""

# # #         # 🔥 IMPORTANT FIX
# # #         return SimpleNamespace(value=text)

# # #     async def a_generate(self, prompt, schema=None, **kwargs):
# # #         return self.generate(prompt, schema)

# # #     def get_model_name(self):
# # #         return MODEL_NAME

# # import requests
# # from deepeval.models.base_model import DeepEvalBaseLLM
# # from types import SimpleNamespace

# # LLM_ENDPOINT = "http://10.41.134.30:8001/v1/chat/completions"
# # MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"


# # class LocalEvalModel(DeepEvalBaseLLM):

# #     def __init__(self):
# #         pass

# #     def load_model(self):
# #         return None

# #     def generate(self, prompt, schema=None, **kwargs):

# #         try:
# #             response = requests.post(
# #                 LLM_ENDPOINT,
# #                 json={
# #                     "model": MODEL_NAME,
# #                     "messages": [
# #                         {"role": "user", "content": prompt}
# #                     ]
# #                 },
# #                 timeout=60
# #             )

# #             response.raise_for_status()
# #             data = response.json()

# #             print("🔍 EVAL LLM RAW:", data)

# #             text = data["choices"][0]["message"]["content"].strip()

# #         except Exception as e:
# #             print("❌ LLM API Error:", e)
# #             text = ""

# #         # 🔥 CRITICAL FIX (DO NOT REMOVE)
# #         if schema is not None:
# #             # GEval metrics expect object with `.value`
# #             return SimpleNamespace(value=text)

# #         # Core metrics expect STRING
# #         return text

# #     async def a_generate(self, prompt, schema=None, **kwargs):
# #         return self.generate(prompt, schema)

# #     def get_model_name(self):
# #         return MODEL_NAME

# import requests
# from deepeval.models.base_model import DeepEvalBaseLLM
# from types import SimpleNamespace

# LLM_ENDPOINT = "http://10.41.134.30:8001/v1/chat/completions"
# MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"


# class LocalEvalModel(DeepEvalBaseLLM):

#     def __init__(self):
#         pass

#     def load_model(self):
#         return None

#     def generate(self, prompt, schema=None, **kwargs):

#         try:
#             response = requests.post(
#                 LLM_ENDPOINT,
#                 json={
#                     "model": MODEL_NAME,
#                     "messages": [
#                         {"role": "user", "content": prompt}
#                     ]
#                 },
#                 timeout=60
#             )

#             response.raise_for_status()
#             data = response.json()

#             print("🔍 EVAL LLM RAW:", data)

#             text = data["choices"][0]["message"]["content"].strip()

#         except Exception as e:
#             print("❌ LLM API Error:", e)
#             text = ""

#         # 🔥 REAL FIX: detect GEval via kwargs
#         is_geval = (
#             "evaluation_params" in kwargs or
#             "criteria" in kwargs or
#             "name" in kwargs
#         )

#         if is_geval:
#             return SimpleNamespace(value=text)

#         return text

#     async def a_generate(self, prompt, schema=None, **kwargs):
#         return self.generate(prompt, schema, **kwargs)

#     def get_model_name(self):
#         return MODEL_NAME
import requests
from deepeval.models.base_model import DeepEvalBaseLLM
from types import SimpleNamespace

LLM_ENDPOINT = "http://10.41.134.30:8001/v1/chat/completions"
MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"


class LocalEvalModel(DeepEvalBaseLLM):

    def load_model(self):
        return None

    def generate(self, prompt, schema=None, **kwargs):

        try:
            response = requests.post(
                LLM_ENDPOINT,
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=60
            )

            response.raise_for_status()
            data = response.json()

            print("🔍 EVAL LLM RAW:", data)

            text = data["choices"][0]["message"]["content"].strip()

        except Exception as e:
            print("❌ LLM API Error:", e)
            text = ""

        # ✅ ALWAYS RETURN STRING (CORE METRICS NEED THIS)
        return text

    async def a_generate(self, prompt, schema=None, **kwargs):
        return self.generate(prompt, schema, **kwargs)

    def get_model_name(self):
        return MODEL_NAME