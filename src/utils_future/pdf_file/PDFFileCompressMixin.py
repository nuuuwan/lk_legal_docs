import io
import shutil

import pymupdf
from PIL import Image
from utils import Log

log = Log("PDFFileCompressMixin")


class PDFFileCompressMixin:
    QUALITY = 70
    SCALE = 0.5

    @classmethod
    def __compress_images__(cls, doc):
        for page in doc:
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                img_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                new_size = (
                    int(img_pil.width * cls.SCALE),
                    int(img_pil.height * cls.SCALE),
                )
                img_pil = img_pil.resize(new_size)

                new_img_bytes = io.BytesIO()
                img_pil.save(
                    new_img_bytes,
                    format="JPEG",
                    quality=cls.QUALITY,
                )
                doc.update_stream(xref, new_img_bytes.getvalue())
        return doc

    def __compress__hot__(self, compressed_pdf_path: str):
        doc = pymupdf.open(self.path)
        doc = self.__compress_images__(doc)
        doc.save(
            compressed_pdf_path,
            garbage=4,
            clean=True,
            deflate=True,
            deflate_images=True,
            deflate_fonts=True,
        )
        doc.close()

    def compress(self, compressed_pdf_path: str):
        self.__compress__hot__(compressed_pdf_path)
        compressed_pdf_file = self.__class__(compressed_pdf_path)
        p_compress = 100 * (1 - compressed_pdf_file.size / self.size)
        if p_compress > 0:
            log.debug(
                f"Compressed {self} -> {compressed_pdf_file}"
                + f" ({p_compress:.1f}%)"
            )
        else:
            log.warning(f"Compression not effective, copying original {self}")
            shutil.copy(self.path, compressed_pdf_path)
        return compressed_pdf_file
