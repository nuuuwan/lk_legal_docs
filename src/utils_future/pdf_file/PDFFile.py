import io
import shutil

import pymupdf
from PIL import Image
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

    def compress(
        self,
        compressed_pdf_path: str,
        image_quality: int = 70,
        scale: float = 0.5,
    ):
        doc = pymupdf.open(self.path)

        for page in doc:
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                img_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                new_size = (
                    int(img_pil.width * scale),
                    int(img_pil.height * scale),
                )
                img_pil = img_pil.resize(new_size)

                new_img_bytes = io.BytesIO()
                img_pil.save(
                    new_img_bytes, format="JPEG", quality=image_quality
                )
                doc.update_stream(xref, new_img_bytes.getvalue())

        doc.save(
            compressed_pdf_path,
            garbage=4,
            clean=True,
            deflate=True,
            deflate_images=True,
            deflate_fonts=True,
        )
        doc.close()

        compressed_pdf_file = PDFFile(compressed_pdf_path)
        p_compress = 100 * (1 - compressed_pdf_file.size / self.size)
        if p_compress > 0:
            log.debug(
                f"Compressed {self} -> {compressed_pdf_file} ({p_compress:.1f}%)"
            )
        else:
            log.warning(f"Compression not effective, copying original {self}")
            shutil.copy(self.path, compressed_pdf_path)
        return compressed_pdf_file
