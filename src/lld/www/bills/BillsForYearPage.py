from lld.www.bills.BillMetadata import BillMetadata
from lld.www.common import ForYearPage


class BillsForYearPage(ForYearPage):
    @classmethod
    def get_doc_type_name(cls):
        return 'bills'

    @classmethod
    def get_doc_metadata_cls(cls):
        return BillMetadata
