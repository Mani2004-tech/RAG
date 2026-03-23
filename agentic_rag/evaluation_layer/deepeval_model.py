from deepeval.models.base_model import DeepEvalBaseLLM
from groq import Groq
import json


class GroqEvalModel(DeepEvalBaseLLM):

    def __init__(self):

        self.client = Groq()

        self.model = "llama-3.1-8b-instant"


    def load_model(self):

        return self.client


    def generate(self, prompt, schema=None, **kwargs):

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            temperature=0

        )

        text=response.choices[0].message.content


        # DeepEval expects structured output if schema exists

        if schema:

            try:

                return schema.parse_raw(text)

            except:

                # fallback minimal valid structure

                return schema.construct()


        return text


    async def a_generate(self, prompt, schema=None, **kwargs):

        return self.generate(prompt, schema=schema)


    def get_model_name(self):

        return "Groq Llama"