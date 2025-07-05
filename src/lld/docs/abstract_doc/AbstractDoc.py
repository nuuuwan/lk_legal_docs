from utils import Log

from lld.docs.abstract_doc.AbstractDocBase import AbstractDocBase
from lld.docs.abstract_doc.AbstractDocReadMe import AbstractDocReadMe
from lld.docs.abstract_doc.AbstractDocSerializer import AbstractDocSerializer

log = Log("AbstractDoc")


class AbstractDoc(AbstractDocBase, AbstractDocSerializer, AbstractDocReadMe):

    @classmethod
    def get_doc_type_name(cls):
        raise NotImplementedError
