from utils import Log

from lk_legal_docs.legal_docs.AbstractGovLkPDFDoc import AbstractGovLkPDFDoc

log = Log("Act")


class Act(AbstractGovLkPDFDoc):

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
                "A legal act is a law passed by Parliament that governs rights, duties, economy, and society, shaping daily life and national policy.",  # noqa: E501
            ]
        )

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "⚖️"

    @classmethod
    def get_url_for_year(cls, year: int) -> str:
        return f"{cls.get_url_base()}/acts_{year}.html"

    @classmethod
    def get_url_index(cls) -> str:
        return f"{cls.get_url_base()}/acts.html"
