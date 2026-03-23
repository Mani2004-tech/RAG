from agentic_rag.reasoning_layer.reasoning_service import ReasoningService


class Doc:

    def __init__(self,text):

        self.content=text


docs=[

Doc("Artificial Intelligence is simulation of human intelligence."),

Doc("AI uses machine learning.")

]

query="What is AI?"

answer="AI is simulation of human intelligence."


service=ReasoningService()

result=service.run(

query,

answer,

docs

)

print("\nFINAL RESULT:\n")

print(result)