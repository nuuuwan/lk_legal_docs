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
        return self.date[:4]

    @cached_property
    def year_and_month(self):
        return self.date[:7]

    @cached_property
    def id(self):
        return self.doc_num.replace("/", "-")

    @classmethod
    def get_doc_type_dir(cls):
        return os.path.join("data", cls.get_doc_type_name())

    @cached_property
    def dir_data(self):
        dir_data = os.path.join(self.get_doc_type_dir(), self.year, self.id)
        os.makedirs(dir_data, exist_ok=True)
        return dir_data
