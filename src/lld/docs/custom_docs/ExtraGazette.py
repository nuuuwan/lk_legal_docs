from lld.docs.abstract_doc import AbstractDoc


class ExtraGazette(AbstractDoc):
    @classmethod
    def get_doc_type_name(cls):
        return "extra-gazettes"

    @classmethod
    def get_doc_type_name_short(cls):
        return "egz"

    @classmethod
    def get_emoji(cls):
        return "🚨"

    @classmethod
    def get_doc_type_name_long(cls):
        return "Extraordinary Gazettes"
