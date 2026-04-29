from langsmith import traceable
from agentic_rag.query_layer.graph.rag_graph import rag_graph


@traceable(name="rag_graph_execution", run_type="chain")
def execute_rag_graph(state):

    # ✅ ROOT TRACE
    

    # ✅ PASS TO GRAPH
    

    result = rag_graph.invoke(state)

    # ✅ END ROOT
   

    return result