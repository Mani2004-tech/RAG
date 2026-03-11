from agentic_rag.query_layer.graph.rag_graph import rag_graph
from agentic_rag.memory.chat_memory import ChatMemory

memory = ChatMemory()


def run_chat(session_id: str, message: str):

    memory.create_session(session_id)

    # store user message
    memory.add_message(session_id, "user", message)

    # load conversation history
    history = memory.get_history(session_id)

    result = rag_graph.invoke({
        "query": message,
        "chat_history": history,
        "session_id": session_id
    })

    answer = result.get("answer", "")

    # store assistant response
    memory.add_message(session_id, "assistant", answer)

    return answer