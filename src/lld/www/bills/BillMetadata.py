from utils import Log

from lld.www.common import Metadata

log = Log('BillMetadata')


class BillMetadata(Metadata):

    @classmethod
    def get_doc_type_name(cls):
        return 'bills'
