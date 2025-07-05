import re

from utils import Log

from lld.docs.custom_docs.Gazette import Gazette
from lld.www.pages import AbstractPipelineRunner
from lld.www_common import WebPage

log = Log("GazettePages")


class GazettePages(AbstractPipelineRunner):

    BASE_URL = "https://documents.gov.lk/view/gazettes/"

    def get_pipeline_name(self):
        return "gazettes"

    def gen_year_pages(self):
        by_year_page = WebPage(GazettePages.BASE_URL + "/find_gazette.html")
        div_year_container = by_year_page.soup.find(
            "div", class_="year-container"
        )
        for a in div_year_container.find_all("a"):
            href = a.get("href")
            url = "/".join([GazettePages.BASE_URL, href])
            yield WebPage(url)

    def gen_gazette_pages(self):
        for year_page in self.gen_year_pages():
            table = year_page.soup.find("table", class_="table")
            tbody = table.find("tbody")
            for tr in tbody.find_all("tr"):
                td_list = tr.find_all("td")
                a = td_list[1].find("a")
                href = a.get("href")
                url = "/".join([GazettePages.BASE_URL, href])
                yield WebPage(url)

    @staticmethod
    def __get_doc_num__(date, description):
        doc_num = re.sub(r"[^a-zA-Z0-9]+", "-", description).lower()
        doc_num = f"{date}-{doc_num}"
        doc_num = re.sub(r"-{2,}", "-", doc_num)
        return doc_num

    @staticmethod
    def __process_li__(li_sub_part, date):
        description = li_sub_part.find("strong").text.strip()
        doc_num = GazettePages.__get_doc_num__(date, description)

        source_url_en, source_url_si, source_url_ta = (None, None, None)
        a_list = li_sub_part.find_all("a")
        for a in a_list:
            if a.has_attr("disabled"):
                continue
            href = a["href"]
            url = "/".join([GazettePages.BASE_URL, href])

            if "E.pdf" in href:
                source_url_en = url
            elif "S.pdf" in href:
                source_url_si = url
            elif "T.pdf" in href:
                source_url_ta = url
            else:
                log.warning(f"Unknown language code in URL: {href}")

        return Gazette(
            doc_num=doc_num,
            date=date,
            description=description,
            source_url_en=source_url_en,
            source_url_si=source_url_si,
            source_url_ta=source_url_ta,
        )

    def gen_docs(self):
        for gazette_page in self.gen_gazette_pages():
            date = gazette_page.url.split("/")[-1].split(".")[0]
            assert len(date) == 10

            part_cards = gazette_page.soup.find_all("div", class_="part-card")
            for part_card in part_cards:
                ul_sub_parts = part_card.find("ul", class_="list-group")
                for li_sub_part in ul_sub_parts.find_all(
                    "li", class_="list-group-item"
                ):
                    yield GazettePages.__process_li__(li_sub_part, date)
