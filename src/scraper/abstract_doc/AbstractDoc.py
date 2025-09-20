from scraper.abstract_doc.core.AbstractDocBase import AbstractDocBase
from scraper.abstract_doc.core.AbstractDocBasePathsMixin import \
    AbstractDocBasePathsMixin
from scraper.abstract_doc.core.AbstractDocGeneratorMixin import \
    AbstractDocGeneratorMixin
from scraper.abstract_doc.core.AbstractDocMetadataMixin import \
    AbstractDocMetadataMixin
from scraper.abstract_doc.core.AbstractDocRemotePathMixin import \
    AbstractDocRemotePathMixin
from scraper.abstract_doc.core.AbstractDocTextMixin import AbstractDocTextMixin
from scraper.abstract_doc.hugging_face import AbstractDocHuggingFaceMixin
from scraper.abstract_doc.pipeline.AbstractDocPipelineMixin import \
    AbstractDocPipelineMixin
from scraper.abstract_doc.readme import AbstractDocReadMeMixin
from scraper.abstract_doc.readme.AbstractDocGlobalReadMeMixin import \
    AbstractDocGlobalReadMeMixin
from scraper.abstract_doc.readme.AbstractDocSummaryMixin import \
    AbstractDocSummaryMixin


class AbstractDoc(
    AbstractDocBase,
    AbstractDocBasePathsMixin,
    AbstractDocGeneratorMixin,
    AbstractDocMetadataMixin,
    AbstractDocRemotePathMixin,
    AbstractDocReadMeMixin,
    AbstractDocSummaryMixin,
    AbstractDocHuggingFaceMixin,
    AbstractDocPipelineMixin,
    AbstractDocGlobalReadMeMixin,
    AbstractDocTextMixin,
):
    pass
