from lld.docs.abstract_doc import AbstractDoc


class Gazette(AbstractDoc):
    @classmethod
    def get_doc_type_name(cls):
        return "gazettes"

    @classmethod
    def get_doc_type_name_short(cls):
        return "find_gazette"

    @classmethod
    def get_emoji(cls):
        return "📢"
