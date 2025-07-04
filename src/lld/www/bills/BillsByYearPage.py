from lld.www.bills.BillsForYearPage import BillsForYearPage
from lld.www.common import ByYearPage


class BillsByYearPage(ByYearPage):
    @classmethod
    def get_doc_type_name(cls):
        return 'bills'

    @classmethod
    def get_doc_type_name_short(cls):
        return 'bl'

    @classmethod
    def get_for_year_page_cls(cls):
        return BillsForYearPage
