import os

from lld.www_common import WebPage


class AbstractDocDownloader:

    def get_pdf_path(self, lang):
        return os.path.join(self.dir_data, f"{lang}.pdf")

    def download_all(self):
        did_hot_download = False
        for lang, url in [
            ("en", self.source_url_en),
            ("si", self.source_url_si),
            ("ta", self.source_url_ta),
        ]:
            if not url:
                continue
            file_path = self.get_pdf_path(lang)
            if not os.path.exists(file_path):
                page = WebPage(url)
                page.download_binary(file_path)
                did_hot_download = True

        return did_hot_download
