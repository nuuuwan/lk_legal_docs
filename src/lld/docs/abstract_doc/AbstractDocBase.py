import os
from dataclasses import dataclass
from functools import cached_property


@dataclass
class AbstractDocBase:
    doc_num: str
    date: str
    description: str
    source_url_en: str
    source_url_si: str
    source_url_ta: str

    @cached_property
    def year(self):
        return self.doc_num.split("/")[1]

    @cached_property
    def year_doc_num(self):
        return self.doc_num.split("/")[0]

    @classmethod
    def get_doc_type_dir(cls):
        return os.path.join("data", cls.get_doc_type_name())

    @cached_property
    def id(self):
        return f"{self.year}-{self.year_doc_num}"
