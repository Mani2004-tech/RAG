import re


class PDFCleaner:

    def clean(self, text):

        text = self.remove_unicode(text)
        text = self.fix_hyphenation(text)
        text = self.normalize_space(text)

        return text

    def remove_unicode(self, text):

        return re.sub(r"[^\x00-\x7F]+", " ", text)

    def fix_hyphenation(self, text):

        return re.sub(r"-\s+", "", text)

    def normalize_space(self, text):

        return re.sub(r"\s+", " ", text).strip()