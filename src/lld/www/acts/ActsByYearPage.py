from lld.www.acts.ActsForYearPage import ActsForYearPage
from lld.www.common import ByYearPage


class ActsByYearPage(ByYearPage):
    @classmethod
    def get_doc_type_name(cls):
        return 'acts'

    @classmethod
    def get_doc_type_name_short(cls):
        return 'acts'

    @classmethod
    def get_for_year_page_cls(cls):
        return ActsForYearPage
