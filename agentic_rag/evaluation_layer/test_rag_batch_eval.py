import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000/query"

queries = [
    # Insurance
    "What are the types of insurance products?",
    "What is life insurance?",
    "What risks are associated with ULIPs?",

    # Mutual Fund
    "What is a mutual fund?",
    "What are the types of mutual funds?",
    "Are mutual funds risky?",

    # Retirement
    "What are retirement planning products?",
    "What are annuities?",
    "What risks exist in retirement planning?",

    # Edge cases
    "What is term insurance?",
    "What is cryptocurrency?",
    "Explain quantum computing"
]

results = []

print("\n🚀 STARTING BATCH EVALUATION\n")

for i, query in enumerate(queries):

    print(f"\n🔹 Query {i+1}: {query}")

    try:
        response = requests.post(API_URL, json={"query": query})
        data = response.json()

        answer = data.get("answer", "")
        evaluation = data.get("evaluation", {})

        print("🧠 Answer:", answer[:150])
        print("📊 Eval:", evaluation)

        results.append({
            "query": query,
            "answer": answer,
            "evaluation": evaluation
        })

    except Exception as e:
        print("❌ Error:", e)
        results.append({
            "query": query,
            "error": str(e)
        })

# ------------------------------
# SAVE RESULTS
# ------------------------------
filename = f"eval_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

with open(filename, "w") as f:
    json.dump(results, f, indent=4)

print("\n✅ Evaluation complete")
print(f"📁 Saved to: {filename}")