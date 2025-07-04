from functools import cache

from lld.www.common.WebPage import WebPage


class ForYearPage(WebPage):
    @classmethod
    def get_doc_type_name(cls):
        raise NotImplementedError

    @classmethod
    def get_doc_metadata_cls(cls):
        raise NotImplementedError

    def __init__(self, url):
        super().__init__(url)

    @classmethod
    def __parse_tr__(cls, tr):
        td_list = tr.find_all("td")
        doc_num = td_list[0].text.strip()
        date = td_list[1].text.strip()
        description = td_list[2].text.strip()
        url_td = td_list[3]
        a_list = url_td.find_all("a")

        source_url_en, source_url_si, source_url_ta = [
            f'https://documents.gov.lk/view/{cls.get_doc_type_name()}/'
            + a['href']
            for a in a_list
        ]

        doc_metadata_cls = cls.get_doc_metadata_cls()
        return doc_metadata_cls(
            doc_num=doc_num,
            date=date,
            description=description,
            source_url_en=source_url_en,
            source_url_si=source_url_si,
            source_url_ta=source_url_ta,
        )

    @cache
    def get_metadata_list(self):
        doc_metadata_list = []
        table = self.soup.find(
            "table", class_="table table-bordered table-striped table-hover"
        )
        tbody = table.find("tbody")

        for tr in tbody.find_all("tr"):
            doc_metadata = self.__parse_tr__(tr)
            doc_metadata_list.append(doc_metadata)

        return doc_metadata_list
