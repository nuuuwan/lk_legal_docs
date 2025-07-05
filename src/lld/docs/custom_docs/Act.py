from lld.docs.abstract_doc import AbstractDoc


class Act(AbstractDoc):
    @classmethod
    def get_doc_type_name(cls):
        return "acts"

    @classmethod
    def get_doc_type_name_short(cls):
        return "acts"

    @classmethod
    def get_emoji(cls):
        return "🏛️"
