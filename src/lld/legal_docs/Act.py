from typing import Generator

from scraper import AbstractPDFDoc


class Act(AbstractPDFDoc):
    @classmethod
    def gen_docs(cls) -> Generator["Act", None, None]:
        pass
