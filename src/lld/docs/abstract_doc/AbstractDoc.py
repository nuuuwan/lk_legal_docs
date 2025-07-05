from utils import Log

from lld.docs.abstract_doc.AbstractDocBase import AbstractDocBase
from lld.docs.abstract_doc.AbstractDocDownloader import AbstractDocDownloader
from lld.docs.abstract_doc.AbstractDocExtract import AbstractDocExtract
from lld.docs.abstract_doc.AbstractDocReadMe import AbstractDocReadMe
from lld.docs.abstract_doc.AbstractDocSerializer import AbstractDocSerializer

log = Log("AbstractDoc")


class AbstractDoc(
    AbstractDocBase,
    AbstractDocSerializer,
    AbstractDocReadMe,
    AbstractDocDownloader,
    AbstractDocExtract,
):

    @classmethod
    def get_doc_type_name(cls):
        raise NotImplementedError

    @classmethod
    def get_doc_type_name_short(cls):
        raise NotImplementedError

    @classmethod
    def get_doc_type_name_long(cls):
        return cls.get_doc_type_name().title()
