# Document Preprocessing Pipeline

A comprehensive pipeline for preprocessing documents, particularly PDFs, for use in RAG (Retrieval-Augmented Generation) systems.

## Features

- **Layout Parsing**: Extracts structural elements from PDFs
- **Text Cleaning**: Removes noise and normalizes text
- **Section Detection**: Identifies document sections
- **Hierarchy Building**: Creates hierarchical document structure
- **Citation Extraction**: Finds citations in text
- **NLP Processing**: Named entity recognition and text analysis
- **PII Detection**: Identifies personally identifiable information
- **Metadata Extraction**: Extracts file and document metadata

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download required NLP models:
   ```python
   python -c "import spacy; spacy.download('en_core_web_sm')"
   ```

## Usage

Run the pipeline on a PDF file:

```bash
python preprocessing_pipeline.py path/to/document.pdf
```

This will generate a JSON file with all processing results.

## Modules

- `config.py`: Configuration settings
- `layout_parser.py`: PDF layout analysis
- `pdf_cleaner.py`: Text cleaning utilities
- `section_detector.py`: Section identification
- `hierarchy_builder.py`: Document hierarchy construction
- `citation_extractor.py`: Citation detection
- `nlp_processor.py`: Natural language processing
- `pii_detector.py`: PII detection
- `metadata_extractor.py`: Metadata extraction
- `preprocessing_pipeline.py`: Main pipeline orchestrator

## Troubleshooting

- **Import errors**: Ensure all dependencies are installed
- **PDF parsing issues**: Check if the PDF is password-protected or corrupted
- **NLP model errors**: Verify that the SpaCy model is downloaded
- **Memory issues**: For large PDFs, consider processing in chunks

## Dependencies

- pdfplumber: PDF text extraction
- PyMuPDF: PDF manipulation
- spaCy: NLP processing
- NLTK: Natural language toolkit
- transformers: Advanced NLP models
- presidio-analyzer: PII detection
- python-docx: Word document processing
- openpyxl: Excel file handling