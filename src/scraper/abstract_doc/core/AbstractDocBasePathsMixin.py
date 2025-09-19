import os
from functools import cached_property


class AbstractDocBasePathsMixin:
    @classmethod
    def get_main_branch_dir_root(cls) -> str:
        # e.g. lk_acts
        return "."

    @classmethod
    def get_data_branch_dir_root(cls) -> str:
        # e.g. ../lk_acts_data
        repo_name = cls.get_repo_name()
        return os.path.join(
            "..",
            f"{repo_name}_data",
        )

    @classmethod
    def get_data_branch_dir_root_data(cls) -> str:
        # e.g. ../lk_acts_data/data
        return os.path.join(
            cls.get_data_branch_dir_root(),
            "data",
        )

    @classmethod
    def get_dir_docs_for_cls_relative(cls) -> str:
        # e.g. data/lk_acts
        return os.path.join(
            "data",
            cls.get_doc_class_label(),
        )

    @classmethod
    def get_dir_docs_for_cls(cls) -> str:
        # e.g. ../lk_acts_data/data/lk_acts
        return os.path.join(
            cls.get_data_branch_dir_root_data(),
            cls.get_doc_class_label(),
        )

    @cached_property
    def dir_doc_relative_to_class(self) -> str:
        # e.g. 1990s/1995/ACT_1995_01
        return os.path.join(
            self.decade,
            self.year,
            self.doc_id,
        )

    @cached_property
    def dir_doc(self) -> str:
        # e.g. ../lk_acts_data/data/lk_acts/1990s/1995/ACT_1995_01
        return os.path.join(
            self.__class__.get_dir_docs_for_cls(),
            self.dir_doc_relative_to_class,
        )

    @cached_property
    def json_path(self) -> str:
        # e.g. ../lk_acts_data/data/lk_acts/1990s/1995/ACT_1995_01/doc.json
        return os.path.join(self.dir_doc, "doc.json")
