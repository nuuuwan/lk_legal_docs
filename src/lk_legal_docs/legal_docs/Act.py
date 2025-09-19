from dataclasses import dataclass
from typing import Generator

from utils import Log, Time, TimeFormat

from scraper import AbstractPDFDoc
from utils_future import WWW

log = Log("Act")


@dataclass
class Act(AbstractPDFDoc):
    doc_number: str

    @classmethod
    def get_url_base(cls) -> str:
        return "https://documents.gov.lk/view/acts"

    @classmethod
    def get_doc_class_label(cls):
        return "lk_acts"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return "\n\n".join(
            [
                "A legal act in Sri Lanka is a law passed by Parliament that governs rights, duties, economy, and society, shaping daily life and national policy.",  # noqa: E501
            ]
        )

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "⚖️"

    @classmethod
    def __parse_tr__(cls, tr, url_metadata) -> "Act":
        tds = tr.find_all("td")
        if len(tds) != 4:
            return
        doc_number = tds[0].text.strip()
        date_str = tds[1].text.strip()
        assert len(date_str) == 10  # YYYY-MM-DD
        description = tds[2].text.strip()
        lang_to_url_pdf = {}
        for a in tds[3].find_all("a"):
            lang = a.text.strip().lower()[:2]
            assert lang in ("si", "ta", "en")
            url_pdf = f'{cls.get_url_base()}/{a["href"]}'
            assert url_pdf.endswith(".pdf")
            lang_to_url_pdf[lang] = url_pdf

        for lang, url_pdf in lang_to_url_pdf.items():
            doc_number_cleaned = doc_number.replace("/", "-").replace(
                " ", "_"
            )
            num = f"{date_str}-{doc_number_cleaned}-{lang}"
            yield cls(
                num=num,
                date_str=date_str,
                description=description,
                url_metadata=url_metadata,
                lang=lang,
                url_pdf=url_pdf,
                doc_number=doc_number,
            )

    @classmethod
    def get_url_for_year(cls, year: int) -> str:
        return f"{cls.get_url_base()}/acts_{year}.html"

    @classmethod
    def gen_docs_for_year(cls, year: int) -> Generator["Act", None, None]:
        url_for_year = cls.get_url_for_year(year)
        www = WWW(url_for_year)
        log.debug(f"Processing {www}")
        soup = www.soup
        if not soup:
            return
        table = soup.find(
            "table", class_="table table-bordered table-striped table-hover"
        )
        for tr in table.find_all("tr"):
            yield from cls.__parse_tr__(tr, url_metadata=url_for_year)

    @classmethod
    def gen_docs(cls) -> Generator["Act", None, None]:
        current_year = int(TimeFormat("%Y").format(Time.now()))
        for year in range(current_year, 1945, -1):
            yield from cls.gen_docs_for_year(year)
