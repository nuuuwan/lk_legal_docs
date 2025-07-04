from lld.www.acts.ActMetadata import ActMetadata
from lld.www.common import ForYearPage


class ActsForYearPage(ForYearPage):
    @classmethod
    def get_doc_type_name(cls):
        return 'acts'

    @classmethod
    def get_doc_metadata_cls(cls):
        return ActMetadata
