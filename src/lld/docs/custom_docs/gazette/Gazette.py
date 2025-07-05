from dataclasses import dataclass

from lld.docs.custom_docs.gazette.GazetteDoc import GazetteDoc


@dataclass
class Gazette:
    date: str
    gazette_docs: list[GazetteDoc]
