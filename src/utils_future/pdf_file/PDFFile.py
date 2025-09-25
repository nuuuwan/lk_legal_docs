import pymupdf
from utils import Log

from utils_future.FileOrDirFuture import FileOrDirFuture
from utils_future.pdf_file.PDFTextMixin import PDFTextMixin

log = Log("PDFFile")


class PDFFile(FileOrDirFuture, PDFTextMixin):

    def __init__(self, path):
        assert path.endswith(".pdf")
        super().__init__(path)

    def download_image(self, i_page: int, image_path: str) -> None:
        doc = pymupdf.open(self.path)
        page = doc[i_page]
        pix = page.get_pixmap()
        pix.save(image_path)
        log.info(f"Wrote image {self} to {image_path}")

    def compress(self, compressed_pdf_path: str) -> None:
        doc = pymupdf.open(self.path)
        doc.save(
            compressed_pdf_path,
            garbage=4,  # remove redundant objects
            deflate=True,  # apply zlib compression to streams
            clean=True,  # clean up unused resources
        )
        compressed_pdf_file = PDFFile(compressed_pdf_path)
        p_compress = 100 * (1 - compressed_pdf_file.size / self.size)
        log.info(
            f"Compressed {self} -> {compressed_pdf_file} ({p_compress:.1f}%)"
        )
        return compressed_pdf_file
