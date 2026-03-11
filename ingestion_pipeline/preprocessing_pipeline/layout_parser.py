import fitz  # PyMuPDF


class LayoutParser:

    def parse(self, pdf_path):

        doc = fitz.open(pdf_path)

        text_pages = []

        for page in doc:

            page_text = page.get_text("text")

            if page_text.strip():
                text_pages.append({
                    "page_number": page.number + 1,
                    "text": page_text
                })

        doc.close()

        full_text = "\n".join([p["text"] for p in text_pages])

        return full_text, text_pages