from lld.docs.abstract_doc import AbstractDoc


class Bill(AbstractDoc):
    @classmethod
    def get_doc_type_name(cls):
        return "bills"
