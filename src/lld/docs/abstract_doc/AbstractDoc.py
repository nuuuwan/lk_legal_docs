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
    DELIM_PAGE = "\n\n...\n\n"

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
            text = self.DELIM_PAGE.join(
                page.extract_text() or "" for page in reader.pages
            )
            File(txt_path).write(text)
            file_size_k = os.path.getsize(txt_path) / 1_000
            log.debug(f"Wrote text to {txt_path} ({file_size_k:.0f} KB)")
