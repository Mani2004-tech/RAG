from agentic_rag.query_layer.graph.rag_graph import rag_graph

query = input("Query: ")

result = rag_graph.invoke({"query": query})

print("\nAnswer:\n")
print(result["answer"])
