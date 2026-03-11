from langsmith import traceable


class LangsmithMonitor:

    @traceable(name="preprocessing")
    def trace_preprocessing(self, text):
        return {"length": len(text)}

    @traceable(name="metadata")
    def trace_metadata(self, metadata):
        return metadata

    @traceable(name="chunking")
    def trace_chunking(self, chunks):
        return {"chunk_count": len(chunks)}

    @traceable(name="indexing")
    def trace_indexing(self, results):
        return results

    @traceable(name="retrieval")
    def trace_retrieval(self, docs):
        return {"docs": len(docs)}

    @traceable(name="answer_generation")
    def trace_answer(self, answer):
        return {"answer": answer}