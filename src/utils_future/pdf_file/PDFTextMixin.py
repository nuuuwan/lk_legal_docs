import re

import pymupdf
from utils import Log

log = Log("PDFTextMixin")


class PDFTextMixin:
    MIN_TEXT_SIZE = 1_000

    @staticmethod
    def __clean_text__(text: str) -> str:
        text = text or ""
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

    @staticmethod
    def __parse_lines_inner__(span, text_parts, fonts, sizes):
        t = span.get("text", "")
        if t:
            text_parts.append(t)
        f = span.get("font")
        if f:
            fonts.add(f)
        s = span.get("size")
        if s is not None:
            sizes.add(s)

    @staticmethod
    def __parse_lines__(b):
        text_parts = []
        fonts = set()
        sizes = set()
        for line in b.get("lines", []):
            for span in line.get("spans", []):
                PDFTextMixin.__parse_lines_inner__(
                    span, text_parts, fonts, sizes
                )
        text = "".join(text_parts)
        text = PDFTextMixin.__clean_text__(text)
        return fonts, sizes, text

    def get_blocks(self):
        doc = pymupdf.open(self.path)
        block_info_list = []
        for page in doc:
            for b in page.get_text("dict").get("blocks", []):
                fonts, sizes, text = self.__parse_lines__(b)
                if not text:
                    continue
                bbox = tuple([round(x, 2) for x in b.get("bbox", [])])

                block_info = dict(
                    page_number=page.number,
                    bbox=bbox,
                    text=text,
                    fonts=sorted(fonts),
                    sizes=sorted(sizes),
                )
                block_info_list.append(block_info)
        return block_info_list
