import pdfplumber


class TableExtractor:

    def extract_tables(self, file_path):

        tables = []

        with pdfplumber.open(file_path) as pdf:

            for page_number, page in enumerate(pdf.pages):

                extracted = page.extract_tables()

                for table in extracted:

                    tables.append({
                        "page": page_number,
                        "table": table
                    })

        return tables