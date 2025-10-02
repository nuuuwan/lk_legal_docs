import os
import tempfile
from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from utils import WWW, File, JSONFile, Log, PDFFile

from scraper.abstract_doc import AbstractDoc

log = Log("AbstractPDFDoc")


@dataclass
class AbstractPDFDoc(AbstractDoc, ABC):
    url_pdf: str

    # PDF
    # ----------------------------------------------------------------
    @cached_property
    def pdf_path(self) -> str:
        return os.path.join(self.dir_doc, "doc.pdf")

    @property
    def has_pdf(self) -> bool:
        return os.path.exists(self.pdf_path)

    def download_pdf(self):
        with tempfile.NamedTemporaryFile(
            suffix=".pdf", delete=False
        ) as temp_pdf_f:
            temp_pdf_path = temp_pdf_f.name
            WWW(self.url_pdf).download_binary(temp_pdf_path)
            PDFFile(temp_pdf_path).compress(self.pdf_path)

    # Blocks (Extracted from PDF)
    # ----------------------------------------------------------------
    @cached_property
    def blocks_path(self) -> str:
        return os.path.join(self.dir_doc, "blocks.json")

    def extract_blocks(self):
        if not os.path.exists(self.pdf_path):
            return
        pdf_file = PDFFile(self.pdf_path)
        blocks = pdf_file.get_blocks()
        JSONFile(self.blocks_path).write(blocks)
        log.info(f"Wrote {self.blocks_path} ({len(blocks):,} blocks)")

        text_lines = [block["text"] for block in blocks if block["text"]]
        File(self.doc_readme_path).write("\n\n".join(text_lines))
        log.info(f"Wrote {self.doc_readme_path}")

    def get_blocks(self):
        if not os.path.exists(self.blocks_path):
            return []
        return JSONFile(self.blocks_path).read()

    def extract_text(self):  # overrides AbstractDocTextMixin
        blocks = self.get_blocks()
        text_list = [block["text"] for block in blocks if block["text"]]
        content = "\n\n".join(text_list)
        File(self.text_path).write(content)
        log.info(f"Wrote {self.text_path}")
        File(self.doc_readme_path).write(content)
        log.info(f"Wrote {self.doc_readme_path}")

    # All
    # ----------------------------------------------------------------
    def scrape_extended_data_for_doc(self):
        if not self.has_pdf:
            self.download_pdf()

        if self.has_pdf:
            if not os.path.exists(self.blocks_path):
                self.extract_blocks()

            if os.path.exists(self.blocks_path) and not os.path.exists(
                self.text_path
            ):
                self.extract_text()
        else:
            # HACK cleanup
            if os.path.exists(self.blocks_path):
                os.remove(self.blocks_path)
            if os.path.exists(self.text_path):
                os.remove(self.text_path)
