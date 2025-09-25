import os
import shutil

from utils import Log

log = Log("AbstractDocPipelineCleanupMixin")


class AbstractDocPipelineCleanupMixin:

    @classmethod
    def cleanup_all(cls):
        # cleanup cls.get_data_branch_dir_root()
        legacy_dir_hugging_face_data = os.path.join(
            cls.get_data_branch_dir_root(), "hugging_face_data"
        )
        if os.path.exists(legacy_dir_hugging_face_data):
            shutil.rmtree(legacy_dir_hugging_face_data)
            log.warning(f"🧹 Deleted {legacy_dir_hugging_face_data}")

        # cleanup get_data_branch_dir_root_data()
        # should only have get_dir_docs_for_cls()
        for child_name in os.listdir(cls.get_data_branch_dir_root_data()):
            child_path = os.path.join(
                cls.get_data_branch_dir_root_data(), child_name
            )
            if child_name != cls.get_doc_class_label():
                if os.path.isdir(child_path):
                    shutil.rmtree(child_path)
                else:
                    os.remove(child_path)
                log.warning(f"🧹 Deleted {child_path}")

        # cleanup cls.get_dir_docs_for_cls()
        if os.path.exists(cls.get_dir_docs_for_cls()):
            for file_name in os.listdir(cls.get_dir_docs_for_cls()):
                if file_name == "docs_by_year_and_lang.png":
                    file_path = os.path.join(
                        cls.get_dir_docs_for_cls(), file_name
                    )
                    os.remove(file_path)
                    log.warning(f"🧹 Deleted {file_path}")
