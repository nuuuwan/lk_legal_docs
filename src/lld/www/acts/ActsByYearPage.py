from functools import cache

from lld.www.acts.ActsForYearPage import ActsForYearPage
from lld.www.common import WebPage


class ActsByYearPage(WebPage):
    def __init__(self):
        super().__init__("https://documents.gov.lk/view/acts/acts.html")

    @cache
    def get_acts_for_year_page_list(self):
        div_buttons = self.soup.find("div", class_="button-container")
        acts_for_year_page_list = []
        for a in div_buttons.find_all("a"):
            href = a.get("href")
            url = self.BASE_URL + '/view/acts/' + href
            acts_for_year_pag = ActsForYearPage(url)
            acts_for_year_page_list.append(acts_for_year_pag)
        return acts_for_year_page_list
