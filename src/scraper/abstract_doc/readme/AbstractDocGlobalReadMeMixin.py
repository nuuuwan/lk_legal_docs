import os
from typing import Generator

from utils import File, JSONFile, Log

log = Log("AbstractDocGlobalReadMeMixin")


class AbstractDocGlobalReadMeMixin:
    GLOBAL_README_PATH = "README.md"

    @classmethod
    def get_summary_path_for_doc_class(cls, doc_class_label: str) -> str:
        # E.g. ../lk_acts_data/data/lk_acts/summary.json
        return os.path.join(
            cls.get_data_branch_dir_root_data(),
            doc_class_label,
            "summary.json",
        )

    @classmethod
    def get_summary_for_doc_class(cls, doc_class_label: str) -> dict:
        return JSONFile(
            cls.get_summary_path_for_doc_class(doc_class_label)
        ).read()

    @classmethod
    def get_lines_for_doc_class(cls, doc_class_label: str) -> list[str]:
        summary = cls.get_summary_for_doc_class(doc_class_label)
        return cls.get_lines_for_header(summary) + cls.get_lines_for_blurb(
            summary
        )

    @classmethod
    def gen_doc_class_labels(cls) -> Generator[str, None, None]:
        root_path = cls.get_data_branch_dir_root_data()
        for child_name in os.listdir(root_path):
            child_path = os.path.join(root_path, child_name)
            if os.path.isdir(child_path):
                yield child_name

    @classmethod
    def get_lines_for_doc_classes(cls) -> list[str]:
        lines = []
        for doc_class_label in cls.gen_doc_class_labels():
            lines.extend(cls.get_lines_for_doc_class(doc_class_label))
        return lines

    @classmethod
    def get_lines(cls) -> list[str]:
        return (
            cls.get_lines_for_doc_classes()
            + ["", "---", ""]
            + cls.get_lines_for_footer()
        )

    @classmethod
    def build_global_readme(cls):
        File(cls.GLOBAL_README_PATH).write_lines(cls.get_lines())
        log.info(f"Wrote {cls.GLOBAL_README_PATH}")
