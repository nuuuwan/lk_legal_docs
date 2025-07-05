from lld.www.common import ForYearPage
from lld.www.extra_gazettes.BillMetadata import BillMetadata


class ExtraGazettesForYearPage(ForYearPage):
    @classmethod
    def get_doc_type_name(cls):
        return "extra-gazettes"

    @classmethod
    def get_doc_metadata_cls(cls):
        return BillMetadata
