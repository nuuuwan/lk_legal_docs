from utils import Log

from lld.www.common import Metadata

log = Log('ActMetadata')


class ActMetadata(Metadata):

    @classmethod
    def get_doc_type_name(cls):
        return 'acts'
