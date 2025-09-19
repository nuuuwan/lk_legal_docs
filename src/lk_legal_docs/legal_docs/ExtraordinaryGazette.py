from dataclasses import dataclass

from lk_legal_docs.legal_docs.Act import Act


@dataclass
class ExtraordinaryGazette(Act):

    @classmethod
    def get_url_base(cls) -> str:
        return "https://documents.gov.lk/view/extra-gazettes"

    @classmethod
    def get_doc_class_label(cls):
        return "lk_extraordinary_gazettes"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return "\n\n".join(
            [
                "An Extraordinary Gazette is an official government publication used to announce urgent laws, regulations, or public notices with immediate effect.",  # noqa: E501
            ]
        )

    @classmethod
    def get_url_for_year(cls, year: int) -> str:
        return f"{cls.get_url_base()}/egz_{year}.html"

    @classmethod
    def get_url_index(cls) -> str:
        return f"{cls.get_url_base()}/egz.html"

    @classmethod
    def build_global_readme(cls):
        pass
