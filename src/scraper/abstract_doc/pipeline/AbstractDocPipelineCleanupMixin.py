import os
import shutil

from utils import Log

log = Log("AbstractDocPipelineCleanupMixin")


class AbstractDocPipelineCleanupMixin:

    @classmethod
    def cleanup_all(cls):
        legacy_dir_hugging_face_data = os.path.join(
            cls.get_data_branch_dir_root(), "hugging_face_data"
        )
        if os.path.exists(legacy_dir_hugging_face_data):
            shutil.rmtree(legacy_dir_hugging_face_data)
            log.warning(f"🧹 Deleted {legacy_dir_hugging_face_data}")

        legacy_chart_docs_by_year_path = os.path.join(
            cls.get_dir_docs_for_cls(), "docs_by_year.png"
        )
        if os.path.exists(legacy_chart_docs_by_year_path):
            os.remove(legacy_chart_docs_by_year_path)
            log.warning(f"🧹 Deleted {legacy_chart_docs_by_year_path}")
