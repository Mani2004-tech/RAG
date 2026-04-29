from agentic_rag.evaluation_layer.evaluation_service import EvaluationService
from haystack import Document  # IMPORTANT

query = "What is term insurance?"

answer = """
Term insurance is a type of life insurance that provides coverage
for a specific period of time and pays a death benefit.
"""

# ------------------------------
# SIMULATED RAG CONTEXT (FROM PDFs)
# ------------------------------
docs = [

    Document(
        content="""
Insurance Product Information:
Types: Life Insurance, Health Insurance, ULIPs.
Suitability: Depends on life stage and financial needs.
"""
    ),

    Document(
        content="""
Mutual Fund Product Information:
A mutual fund pools money from investors to invest in equities, debt, or hybrid assets.
Returns are market-linked and suitable for long-term goals.
"""
    ),

    Document(
        content="""
Retirement Planning Product Overview:
Product Categories: Pension Plans, Annuities, Retirement Mutual Funds.
Objectives include income post-retirement and capital preservation.
"""
    )
]

# ------------------------------
# RUN EVALUATION
# ------------------------------
service = EvaluationService()

result = service.run(
    query,
    answer,
    docs
)

print("\nFINAL RESULT:\n")
print(result)