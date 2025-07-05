from utils import Log

from lld.www_common import WebPage

log = Log("ForYearPage")


class ForYearPage(WebPage):
    @staticmethod
    def __get_base_url__(doc_cls):
        return "/".join(
            [WebPage.BASE_URL, "view", doc_cls.get_doc_type_name()]
        )

    def __init__(self, url, doc_cls):
        super().__init__(url)
        self.doc_cls = doc_cls

    def __parse_tr__(self, tr):
        td_list = tr.find_all("td")
        doc_num = td_list[0].text.strip()
        date = td_list[1].text.strip()
        description = td_list[2].text.strip()
        url_td = td_list[3]
        a_list = url_td.find_all("a")

        source_url_en, source_url_si, source_url_ta = None, None, None
        for a in a_list:
            href = a["href"]
            url = "/".join(
                [
                    ForYearPage.__get_base_url__(self.doc_cls),
                    href,
                ]
            )

            if "E.pdf" in href:
                source_url_en = url
            elif "S.pdf" in href:
                source_url_si = url
            elif "T.pdf" in href:
                source_url_ta = url
            else:
                log.warning(f"Unknown language code in URL: {href}")

        return self.doc_cls(
            doc_num=doc_num,
            date=date,
            description=description,
            source_url_en=source_url_en,
            source_url_si=source_url_si,
            source_url_ta=source_url_ta,
        )

    def gen_docs(self):

        table = self.soup.find(
            "table", class_="table table-bordered table-striped table-hover"
        )
        tbody = table.find("tbody")

        for tr in tbody.find_all("tr"):
            doc = self.__parse_tr__(tr)
            if not doc:
                continue
            yield doc
