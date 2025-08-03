import os
from functools import cached_property

from utils import File, Log

from lld.www_common import WebPage
from utils_future import PDF, Lang

log = Log("AbstractDocPDFDownloader")


class AbstractDocPDFDownloader:
    def get_pdf_path(self, lang_code):
        assert isinstance(lang_code, str)
        return os.path.join(self.dir_temp_data, f"{lang_code}.pdf")

    def get_fail_pdf_path(self, lang_code):
        assert isinstance(lang_code, str)
        return os.path.join(self.dir_temp_data, f"{lang_code}.pdf.fail")

    @staticmethod
    def __download_pdf_helper__(url, file_path):
        page = WebPage(url)
        try:
            page.download_binary(file_path)
            return True
        except Exception as e:
            log.error(f"Download {url} failed: {e}")
            return False

    def __download_pdf__(self, lang_code, url):
        file_path = self.get_pdf_path(lang_code)
        if os.path.exists(file_path):
            return

        if AbstractDocPDFDownloader.__download_pdf_helper__(url, file_path):
            PDF(file_path).compress()
            if PDF(file_path).is_valid():
                log.debug(f"Wrote {file_path}")
                return True

        fail_file_path = self.get_fail_pdf_path(lang_code)
        File(fail_file_path).write(self.id)
        log.debug(f"Wrote {fail_file_path}")
        return False

    def download_pdfs(self):
        did_hot_download = False
        for lang_code, url in self.lang_to_source_url.items():
            if self.__download_pdf__(lang_code, url):
                did_hot_download = True
        return did_hot_download

    @cached_property
    def n_pdfs(self):
        n_pdfs = 0
        for lang in Lang.list_all():
            pdf_path = self.get_pdf_path(lang.code)
            if os.path.exists(pdf_path):
                n_pdfs += 1
        return n_pdfs

    @cached_property
    def n_pdfs_fail(self):
        n_pdfs_fail = 0
        for lang in Lang.list_all():
            fail_pdf_path = self.get_fail_pdf_path(lang.code)
            if os.path.exists(fail_pdf_path):
                n_pdfs_fail += 1
        return n_pdfs_fail
