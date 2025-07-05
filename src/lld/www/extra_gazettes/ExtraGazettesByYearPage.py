from lld.www.common import ByYearPage
from lld.www.extra_gazettes.ExtraGazettesForYearPage import \
    ExtraGazettesForYearPage


class ExtraGazettesByYearPage(ByYearPage):
    @classmethod
    def get_doc_type_name(cls):
        return "extra-gazettes"

    @classmethod
    def get_doc_type_name_short(cls):
        return "egz"

    @classmethod
    def get_for_year_page_cls(cls):
        return ExtraGazettesForYearPage
