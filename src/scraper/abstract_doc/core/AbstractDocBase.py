import os
import re
from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from utils import Hash, Log

log = Log("AbstractDocBase")


@dataclass
class AbstractDocBase(ABC):
    num: str
    date_str: str
    description: str
    url_metadata: str
    lang: str

    @classmethod
    def get_repo_name(cls) -> str:
        return os.path.basename(os.getcwd())

    @classmethod
    def get_doc_class_label(cls) -> str:
        # If the repo has multiple document classes, then override this method
        return cls.get_repo_name()

    @classmethod
    def get_doc_class_description(cls) -> str:
        return f"A collection of {cls.get_doc_class_label()} documents."

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "📄"

    @cached_property
    def num_short(self):
        if len(self.num) < 32:
            return self.num
        h = Hash.md5(self.num)
        return f"{self.num[:23]}-{h[:8]}"

    @cached_property
    def doc_id(self):
        doc_id = f"{self.date_str}-{self.num_short}"
        doc_id = re.sub(r"[^a-zA-Z0-9\-]", "-", doc_id)
        return doc_id

    @cached_property
    def decade(self) -> str:
        assert len(self.date_str) == 10
        return self.date_str[:3] + "0s"

    @cached_property
    def year(self) -> str:
        assert len(self.date_str) == 10
        return self.date_str[:4]
