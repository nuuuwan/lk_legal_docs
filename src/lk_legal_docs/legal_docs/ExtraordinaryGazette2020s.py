from functools import cache

from lk_legal_docs.legal_docs.ExtraordinaryGazette import ExtraordinaryGazette


class ExtraordinaryGazette2020s(ExtraordinaryGazette):
    @classmethod
    @cache
    def get_shard_decade(cls):
        return "2020s"
