import os
from functools import cached_property

from utils import Log

log = Log("AbstractDocRemotePathMixin")


class AbstractDocRemotePathMixin:
    @classmethod
    def get_remote_repo_url(cls) -> str:
        assert os.environ["GITHUB_USERNAME"]
        # E.g. https://github.com/nuuuwan/lk_acts
        return "/".join(
            [
                "https://github.com",
                os.environ["GITHUB_USERNAME"],
                cls.get_doc_class_label(),
            ]
        )

    @classmethod
    def get_remote_data_url_base(cls) -> str:
        assert os.environ["GITHUB_USERNAME"]
        # E.g. https://github.com/nuuuwan/lk_acts/tree/data
        return "/".join(
            [
                cls.get_remote_repo_url(),
                "tree",
                "data",
            ]
        )

    @classmethod
    def get_remote_data_url_for_class(cls) -> str:
        # E.g. https://github.com/nuuuwan/lk_acts/tree/data/lk_acts
        return "/".join(
            [
                cls.get_remote_data_url_base(),
                cls.get_dir_docs_for_cls_relative(),
            ]
        )

    @cached_property
    def remote_data_url(self) -> str:
        return "/".join(
            [
                self.__class__.get_remote_data_url_for_class(),
                self.dir_doc_relative_to_class,
            ]
        )
