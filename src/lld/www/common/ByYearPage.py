from functools import cache

from utils import Log

from lld.www.common.WebPage import WebPage

log = Log('ByYearPage')


class ByYearPage(WebPage):

    @classmethod
    def get_doc_type_name(cls):
        raise NotImplementedError

    @classmethod
    def get_doc_type_name_short(cls):
        raise NotImplementedError

    @classmethod
    def get_for_year_page_cls(cls):
        return NotImplementedError

    def __init__(self):
        super().__init__(
            f"{WebPage.BASE_URL}/view"
            + f"/{self.get_doc_type_name()}"
            + f"/{self.get_doc_type_name_short()}.html"
        )

    @cache
    def get_for_year_page_list(self):
        div_buttons = self.soup.find("div", class_="button-container")
        for_year_page_list = []
        for_year_page_cls = self.get_for_year_page_cls()
        for a in div_buttons.find_all("a"):
            href = a.get("href")
            url = self.BASE_URL + f"/view/{self.get_doc_type_name()}/" + href
            for_year_page = for_year_page_cls(url)
            for_year_page_list.append(for_year_page)
        return for_year_page_list

    def run_pipeline(self, max_n_hot):
        for_year_page_list = self.get_for_year_page_list()
        n = 0
        n_hot = 0
        for for_year_page in for_year_page_list:
            metadata_list = for_year_page.get_metadata_list()
            for metadata in metadata_list:
                if n_hot >= max_n_hot:
                    log.info(f'🛑 Downloaded {n_hot} new acts.')
                    return

                is_hot = metadata.download_all()
                logger = log.info if is_hot else log.debug
                emoji = '🟢' if is_hot else '⚪️'
                logger(f'{emoji} {n_hot}/{max_n_hot}) {metadata.doc_num}')
                metadata.write()
                n += 1
                if is_hot:
                    n_hot += 1
