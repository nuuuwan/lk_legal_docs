from utils import Log

from lld.www.gazette import GazettePages
from lld.www.pages.AbstractPipelineRunner import AbstractPipelineRunner
from lld.www.pages.ForYearPage import ForYearPage
from lld.www_common import WebPage

log = Log("ByYearPage")


class ByYearPage(WebPage, AbstractPipelineRunner):

    def get_pipeline_name(self):
        return self.doc_cls.get_doc_type_name()

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
        if not div_buttons:
            return
        for a in div_buttons.find_all("a"):
            href = a.get("href")
            url = "/".join([ForYearPage.__get_base_url__(self.doc_cls), href])
            yield ForYearPage(url, self.doc_cls)

    def gen_docs(self):
        for for_year_page in self.gen_for_year_pages():
            for doc in for_year_page.gen_docs():
                yield doc

    def run_pipeline(self, max_n_hot):
        if self.doc_cls.get_doc_type_name == "gazette":
            GazettePages().run_pipeline(max_n_hot)
        return super().run_pipeline(max_n_hot)
