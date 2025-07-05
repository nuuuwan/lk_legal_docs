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

    def gen_for_year_pages(self):
        div_buttons = self.soup.find("div", class_="button-container")
        for a in div_buttons.find_all("a"):
            href = a.get("href")
            url = "/".join([ForYearPage.__get_base_url__(self.doc_cls), href])
            yield ForYearPage(url, self.doc_cls)

    def gen_docs(self):
        for for_year_page in self.gen_for_year_pages():
            for doc in for_year_page.gen_docs():
                yield doc

    @staticmethod
    def __process_doc__(doc):

        try:
            is_hot = doc.download_all()
            doc.write()
            doc.write_readme()
            doc.extract_text()
            return is_hot
        except Exception as e:
            log.error(f"❌ Error downloading {doc.doc_num}: {e}")
            return False

    def run_pipeline(self, max_n_hot):
        log.info(
            f"🤖 Running pipeline for {
                self.doc_cls.get_doc_type_name().title()}."
        )
        n_hot = 0
        for doc in self.gen_docs():
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
