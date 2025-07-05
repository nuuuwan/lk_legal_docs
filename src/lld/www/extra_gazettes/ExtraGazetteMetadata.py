from utils import Log

from lld.www.common import Metadata

log = Log("ExtraGazetteMetadata")


class ExtraGazetteMetadata(Metadata):

    @classmethod
    def get_doc_type_name(cls):
        return "extra-gazettes"
