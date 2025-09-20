import sys

from utils import Log

from scraper.abstract_doc.pipeline.AbstractDocPipelineCleanupMixin import \
    AbstractDocPipelineCleanupMixin  # noqa: E501
from scraper.abstract_doc.pipeline.AbstractDocPipelineExtendedDataMixin import \
    AbstractDocPipelineExtendedDataMixin  # noqa: E501
from scraper.abstract_doc.pipeline.AbstractDocPipelineMetadataMixin import \
    AbstractDocPipelineMetadataMixin  # noqa: E501

log = Log("AbstractDocPipelineMixin")


class AbstractDocPipelineMixin(
    AbstractDocPipelineMetadataMixin,
    AbstractDocPipelineExtendedDataMixin,
    AbstractDocPipelineCleanupMixin,
):
    MAX_DT = 750.0

    @classmethod
    def run_pipeline(cls, max_dt=None):
        max_dt = (
            max_dt
            or (float(sys.argv[1]) if len(sys.argv) > 1 else None)
            or AbstractDocPipelineMixin.MAX_DT
        )
        log.debug(f"{max_dt=}s")
        cls.cleanup_all()
        cls.scrape_all_metadata(max_dt)
        cls.scrape_all_extended_data(max_dt)
        cls.build_summary()
        cls.build_doc_class_readme()
        cls.build_and_upload_to_hugging_face()
        cls.build_global_readme()
