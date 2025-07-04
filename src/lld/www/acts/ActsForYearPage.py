from functools import cache

from lld.www.acts.ActMetadata import ActMetadata
from lld.www.common import WebPage


class ActsForYearPage(WebPage):
    def __init__(self, url):
        super().__init__(url)

    @staticmethod
    def __parse_tr__(tr):
        td_list = tr.find_all("td")
        act_num = td_list[0].text.strip()
        date = td_list[1].text.strip()
        description = td_list[2].text.strip()
        url_td = td_list[3]
        a_list = url_td.find_all("a")

        source_url_en, source_url_si, source_url_ta = [
            'https://documents.gov.lk/view/acts/' + a['href'] for a in a_list
        ]

        return ActMetadata(
            act_num=act_num,
            date=date,
            description=description,
            source_url_en=source_url_en,
            source_url_si=source_url_si,
            source_url_ta=source_url_ta,
        )

    @cache
    def get_act_metadata_list(self):
        act_metadata_list = []
        table = self.soup.find(
            "table", class_="table table-bordered table-striped table-hover"
        )
        tbody = table.find("tbody")

        for tr in tbody.find_all("tr"):
            act_metadata = self.__parse_tr__(tr)
            act_metadata_list.append(act_metadata)

        return act_metadata_list
