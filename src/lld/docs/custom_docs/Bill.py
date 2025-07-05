from lld.docs.abstract_doc import AbstractDoc


class Bill(AbstractDoc):
    @classmethod
    def get_doc_type_name(cls):
        return "bills"

    @classmethod
    def get_doc_type_name_short(cls):
        return "bl"

    @classmethod
    def get_emoji(cls):
        return "✍️"
