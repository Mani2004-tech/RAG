# from .layout_parser import LayoutParser
# from .pdf_cleaner import PDFCleaner
# from .section_detector import SectionDetector
# from .hierarchy_builder import HierarchyBuilder
# from .citation_extractor import CitationExtractor
# from .nlp_processor import NLPProcessor
# from .pii_detector import PIIDetector
# from .metadata_extractor import MetadataExtractor
# from .table_extractor import TableExtractor

# class PreprocessingPipeline:

#     def __init__(self):

#         self.parser = LayoutParser()
#         self.cleaner = PDFCleaner()
#         self.section_detector = SectionDetector()
#         self.hierarchy = HierarchyBuilder()
#         self.citations = CitationExtractor()
#         self.nlp = NLPProcessor()
#         self.pii = PIIDetector()
#         self.metadata = MetadataExtractor()
#         self.tables = TableExtractor()

#     def run(self, pdf_path):

#         # -----------------------------
#         # Parse PDF
#         # -----------------------------
#         full_text, parsed_pages = self.parser.parse(pdf_path)

#         if not parsed_pages:
#             print("⚠ PDF parser returned no pages")
#             return "", {"sentences": []}

#         text = "\n".join([p["text"] for p in parsed_pages if p.get("text")])
        

#         if not text.strip():
#             print("⚠ No text extracted from PDF")
#             return "", {"sentences": []}

#         # -----------------------------
#         # Cleaning
#         # -----------------------------
#         text = self.cleaner.clean(text)

#         if not text.strip():
#             print("⚠ Text became empty after cleaning")
#             return "", {"sentences": []}
        
#         tables = self.tables.extract_tables(pdf_path)

#         print("📊 Extracted tables:", len(tables))

#         # -----------------------------
#         # PII Detection
#         # -----------------------------
#         text, pii = self.pii.detect(text)

#         # -----------------------------
#         # Section Detection
#         # -----------------------------
#         sections = self.section_detector.detect(text)

#         # -----------------------------
#         # Hierarchical Tree
#         # -----------------------------
#         tree = self.hierarchy.build(sections)

#         # -----------------------------
#         # Citation Extraction
#         # -----------------------------
#         citations = self.citations.extract(text)

#         # -----------------------------
#         # NLP Processing
#         # -----------------------------
#         nlp_output = self.nlp.process(text)

#         sentences = nlp_output.get("sentences", [])

#         if not sentences:
#             print("⚠ NLP produced no sentences")

#         # -----------------------------
#         # LLM Metadata Extraction
#         # -----------------------------
#         try:
#             llm_metadata = self.metadata.extract(text)
#         except Exception as e:

#             print("⚠ Metadata extraction failed:", e)

#             llm_metadata = {
#                 "keywords": [],
#                 "topic": "",
#                 "summary": ""
#             }

#         # -----------------------------
#         # Build Metadata
#         # -----------------------------
#         metadata = {
#             "entities": nlp_output.get("entities", []),
#             "noun_phrases": nlp_output.get("noun_phrases", []),
#             "sentences": sentences,
#             "citations": citations,
#             "document_tree": tree,
#             "pii": pii,
#             "keywords": llm_metadata.get("keywords", []),
#             "topic": llm_metadata.get("topic", ""),
#             "summary": llm_metadata.get("summary", "")
#         }

#         # Debug logging
#         print("Processed text length:", len(text))
#         print("Sentence count:", len(sentences))

#         return nlp_output.get("processed_text", text), metadata


# if __name__ == "__main__":

#     pipeline = PreprocessingPipeline()

#     processed_text, metadata = pipeline.run("test.pdf")

#     print(processed_text)
#     print(metadata)

from .layout_parser import LayoutParser
from .pdf_cleaner import PDFCleaner
from .section_detector import SectionDetector
from .hierarchy_builder import HierarchyBuilder
from .citation_extractor import CitationExtractor
from .nlp_processor import NLPProcessor
from .pii_detector import PIIDetector
from .metadata_extractor import MetadataExtractor
from .table_extractor import TableExtractor


class PreprocessingPipeline:

    def __init__(self):

        print("⚙ Initializing Preprocessing Pipeline")

        self.parser = LayoutParser()
        self.cleaner = PDFCleaner()
        self.section_detector = SectionDetector()
        self.hierarchy = HierarchyBuilder()
        self.citations = CitationExtractor()
        self.nlp = NLPProcessor()
        self.pii = PIIDetector()
        self.metadata = MetadataExtractor()
        self.tables = TableExtractor()

    def run(self, pdf_path):

        print(f"📄 Processing file: {pdf_path}")

        # -----------------------------
        # Parse PDF
        # -----------------------------

        full_text, parsed_pages = self.parser.parse(pdf_path)

        if not parsed_pages:
            print("⚠ PDF parser returned no pages")
            return "", {"sentences": []}

        text = "\n".join([p["text"] for p in parsed_pages if p.get("text")])

        if not text.strip():
            print("⚠ No text extracted from PDF")
            return "", {"sentences": []}

        # -----------------------------
        # Cleaning
        # -----------------------------

        text = self.cleaner.clean(text)

        if not text.strip():
            print("⚠ Text became empty after cleaning")
            return "", {"sentences": []}

        # -----------------------------
        # Table Extraction
        # -----------------------------

        tables = self.tables.extract_tables(pdf_path)

        print(f"📊 Extracted {len(tables)} tables")

        # -----------------------------
        # PII Detection
        # -----------------------------

        text, pii = self.pii.detect(text)

        # -----------------------------
        # Section Detection
        # -----------------------------

        sections = self.section_detector.detect(text)

        # -----------------------------
        # Hierarchy Building
        # -----------------------------

        tree = self.hierarchy.build(sections)

        # -----------------------------
        # Citation Extraction
        # -----------------------------

        citations = self.citations.extract(text)

        # -----------------------------
        # NLP Processing
        # -----------------------------

        nlp_output = self.nlp.process(text)

        sentences = nlp_output.get("sentences", [])

        if not sentences:
            print("⚠ NLP produced no sentences")

        # -----------------------------
        # LLM Metadata Extraction
        # -----------------------------

        try:
            llm_metadata = self.metadata.extract(text)

        except Exception as e:

            print("⚠ Metadata extraction failed:", e)

            llm_metadata = {
                "keywords": [],
                "topic": "",
                "summary": ""
            }

        # -----------------------------
        # Metadata Object
        # -----------------------------

        metadata = {

            "entities": nlp_output.get("entities", []),
            "noun_phrases": nlp_output.get("noun_phrases", []),
            "sentences": sentences,
            "citations": citations,
            "document_tree": tree,
            "tables": tables,
            "pii": pii,
            "keywords": llm_metadata.get("keywords", []),
            "topic": llm_metadata.get("topic", ""),
            "summary": llm_metadata.get("summary", "")

        }

        print("✅ Preprocessing complete")
        print("Processed text length:", len(text))
        print("Sentence count:", len(sentences))

        return nlp_output.get("processed_text", text), metadata