import os

from pypdf import PdfReader
from utils import File, Log

from lld.docs.abstract_doc.AbstractDocBase import AbstractDocBase
from lld.docs.abstract_doc.AbstractDocDownloader import AbstractDocDownloader
from lld.docs.abstract_doc.AbstractDocReadMe import AbstractDocReadMe
from lld.docs.abstract_doc.AbstractDocSerializer import AbstractDocSerializer

log = Log("AbstractDoc")


class AbstractDoc(
    AbstractDocBase,
    AbstractDocSerializer,
    AbstractDocReadMe,
    AbstractDocDownloader,
):

    @classmethod
    def get_doc_type_name(cls):
        raise NotImplementedError

    @classmethod
    def get_doc_type_name_short(cls):
        raise NotImplementedError

    def extract_text(self):
        pdf_path = self.get_pdf_path("en")
        assert os.path.exists(pdf_path)
        txt_path = os.path.join(self.dir_data, "en.txt")

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
