import os

from pypdf import PdfReader
from utils import File, Log

log = Log("AbstractDocExtract")


class AbstractDocExtract:
    LANGS = ["en", "si", "ta"]

    def extract_text(self):
        for lang in AbstractDocExtract.LANGS:
            self.__extract_text_for_lang__(lang)

    def __extract_text_for_lang__(self, lang):
        pdf_path = self.get_pdf_path(lang)
        assert os.path.exists(pdf_path)
        txt_path = pdf_path[:-4] + ".txt"

        if not os.path.exists(txt_path):
            reader = PdfReader(pdf_path)

            sections = []
            for i_page, page in enumerate(reader.pages, start=1):
                sections.append(f"\n\n<!-- page {i_page} -->\n\n")
                sections.append(page.extract_text() or "")

            content = "".join(sections)
            File(txt_path).write(content)
            file_size_k = os.path.getsize(txt_path) / 1_000
            log.debug(f"Wrote text to {txt_path} ({file_size_k:.0f} KB)")
