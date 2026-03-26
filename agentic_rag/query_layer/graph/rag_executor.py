from langsmith import traceable
from agentic_rag.query_layer.graph.rag_graph import rag_graph


@traceable(name="rag_graph_execution", run_type="chain")
def execute_rag_graph(state):
    return rag_graph.invoke(state)