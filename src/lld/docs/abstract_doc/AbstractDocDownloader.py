import os

from lld.www.common.WebPage import WebPage


class AbstractDocDownloader:
    def download_all(self):
        did_hot_download = False
        for lang, url in [
            ("en", self.source_url_en),
            ("si", self.source_url_si),
            ("ta", self.source_url_ta),
        ]:
            if not url:
                continue
            file_path = os.path.join(self.dir_data, f"{lang}.pdf")
            if not os.path.exists(file_path):
                page = WebPage(url)
                page.download_binary(file_path)
                did_hot_download = True

        return did_hot_download
