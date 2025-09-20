import os
from functools import cached_property

from utils import Log

log = Log("AbstractDocRemotePathMixin")


class AbstractDocRemotePathMixin:

    @classmethod
    def get_github_username(cls) -> str:
        assert os.environ["GITHUB_USERNAME"]
        return os.environ["GITHUB_USERNAME"]

    @classmethod
    def get_remote_repo_url(cls) -> str:
        # E.g. https://github.com/nuuuwan/lk_acts
        return "/".join(
            [
                "https://github.com",
                cls.get_github_username(),
                cls.get_repo_name(),
            ]
        )

    @classmethod
    def get_remote_data_url_base(cls) -> str:
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

    @classmethod
    def get_raw_remote_data_branch_url(cls) -> str:
        # E.g. https://raw.githubusercontent.com/nuuuwan/lk_appeal_court_judgements/refs/heads/data # noqa: E501
        return "/".join(
            [
                "https://raw.githubusercontent.com",
                cls.get_github_username(),
                cls.get_repo_name(),
                "refs",
                "heads",
                "data",
            ]
        )
