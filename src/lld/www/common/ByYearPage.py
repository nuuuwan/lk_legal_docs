from utils import Log

from lld.www.common.ForYearPage import ForYearPage
from lld.www.common.WebPage import WebPage

log = Log("ByYearPage")


class ByYearPage(WebPage):

    @staticmethod
    def __get_url__(doc_cls):
        return "/".join(
            [
                ForYearPage.__get_base_url__(doc_cls),
                doc_cls.get_doc_type_name_short() + ".html",
            ]
        )

    def __init__(self, doc_cls):
        super().__init__(ByYearPage.__get_url__(doc_cls))
        self.doc_cls = doc_cls

    def get_for_year_page_list(self):
        div_buttons = self.soup.find("div", class_="button-container")
        for_year_page_list = []

        for a in div_buttons.find_all("a"):
            href = a.get("href")
            url = "/".join([ForYearPage.__get_base_url__(self.doc_cls), href])
            for_year_page = ForYearPage(url, self.doc_cls)
            for_year_page_list.append(for_year_page)
        return for_year_page_list

    @staticmethod
    def __process_doc__(doc):

        try:
            is_hot = doc.download_all()
            if is_hot:
                doc.write()
                doc.write_readme()
            doc.extract_text()  # HACK! This must be moved into is_hot
            return is_hot
        except Exception as e:
            log.error(f"❌ Error downloading {doc.doc_num}: {e}")
            return False

    def run_pipeline(self, max_n_hot):
        log.info(
            f"🤖 Running pipeline for {self.doc_cls.get_doc_type_name().title()}."
        )
        for_year_page_list = self.get_for_year_page_list()
        n_hot = 0
        for for_year_page in for_year_page_list:
            doc_list = for_year_page.get_doc_list()
            for doc in doc_list:
                if n_hot >= max_n_hot:
                    log.info(f"🛑 Downloaded {n_hot} new docs.")
                    return

                is_hot = self.__process_doc__(doc)
                if is_hot:
                    n_hot += 1
                    log.info(f"✅ ({n_hot}/{max_n_hot}) Downloaded {doc}")
        log.info(
            f"🛑🛑 Downloaded ALL {self.doc_cls.get_doc_type_name().title()}."
        )
