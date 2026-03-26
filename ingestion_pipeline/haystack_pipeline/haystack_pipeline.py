# from haystack import Pipeline
# from haystack.components.preprocessors import DocumentCleaner
# from haystack.components.preprocessors import DocumentSplitter
# from haystack.dataclasses import Document


# class HaystackProcessor:

#     def __init__(self):

#         print("⚙ Initializing Haystack v2 pipeline")

#         self.cleaner = DocumentCleaner()
#         self.splitter = DocumentSplitter(
#             split_by="word",
#             split_length=200,
#             split_overlap=50
#         )

#         self.pipeline = Pipeline()

#         self.pipeline.add_component("cleaner", self.cleaner)
#         self.pipeline.add_component("splitter", self.splitter)

#         self.pipeline.connect("cleaner.documents", "splitter.documents")

#     def process(self, texts):

#         docs = [Document(content=t) for t in texts]

#         result = self.pipeline.run({
#             "cleaner": {"documents": docs}
#         })

#         split_docs = result["splitter"]["documents"]

#         return [d.content for d in split_docs]
from langsmith import traceable
from haystack import Pipeline
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.preprocessors import DocumentSplitter
from haystack.dataclasses import Document


class HaystackProcessor:

    def __init__(self):

        print("⚙ Initializing Haystack v2 pipeline")

        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter(
            split_by="word",
            split_length=200,
            split_overlap=50
        )

        self.pipeline = Pipeline()

        self.pipeline.add_component("cleaner", self.cleaner)
        self.pipeline.add_component("splitter", self.splitter)

        self.pipeline.connect("cleaner.documents", "splitter.documents")

    @traceable(name="haystack_processing", run_type="chain")
    def process(self, texts):

        docs = [Document(content=t) for t in texts]

        result = self.pipeline.run({
            "cleaner": {"documents": docs}
        })

        split_docs = result["splitter"]["documents"]

        return [d.content for d in split_docs]