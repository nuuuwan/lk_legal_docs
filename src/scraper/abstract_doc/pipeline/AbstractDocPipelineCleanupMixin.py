import os
import shutil

from utils import JSONFile, Log

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
