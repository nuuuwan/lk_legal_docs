from functools import cache

from lld.www.common.WebPage import WebPage


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
