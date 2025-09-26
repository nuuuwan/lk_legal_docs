from functools import cached_property

from utils import File, Log

from scraper.abstract_doc.readme.AbstractDocReadMeMixin import \
    AbstractDocReadMeMixin
from scraper.global_readme.GlobalReadMeSummaryMixin import \
    GlobalReadMeSummaryMixin
from utils_future import FileOrDirFuture

log = Log("GlobalReadMe")


class GlobalReadMe(GlobalReadMeSummaryMixin):
    PATH = "README.md"

    def __init__(self, repo_to_doc_classes: dict[str, list[str]]):
        self.repo_to_doc_classes = repo_to_doc_classes
        self.summary_list = self.get_summary_list()
        self.global_summary = self.get_global_summary(self.summary_list)

    @cached_property
    def lines_for_global_summary(self) -> list[str]:
        log.debug(f"global_summary={self.global_summary}")
        all_dataset_size_humanized = FileOrDirFuture.humanize_size(
            self.global_summary["all_dataset_size"]
        )
        return [
            f"**{self.global_summary['n_datasets']:,}** datasets, "
            + f"with **{self.global_summary['n_docs']:,}** documents"
            + f" (**{all_dataset_size_humanized}**).",
            "",
        ]

    def get_lines_for_dataset(self, i_dataset, summary) -> list[str]:
        header_lines = AbstractDocReadMeMixin.get_lines_for_header(summary)
        first_header_line = header_lines[0]
        first_header_line = f"## {i_dataset:03d} " + (
            first_header_line.replace("#SriLanka 🇱🇰", "")
            .replace("`Dataset`", "")
            .strip()[2:]
        )
        header_lines[0] = first_header_line
        return (
            header_lines
            + AbstractDocReadMeMixin.get_lines_for_blurb(summary)
            + AbstractDocReadMeMixin.get_lines_chart_docs_by_year_and_lang(
                summary
            )
        )

    @cached_property
    def lines_for_datasets(self) -> list[str]:
        lines = []
        for i_dataset, summary in enumerate(self.summary_list, start=1):
            lines.extend(self.get_lines_for_dataset(i_dataset, summary))
        return lines

    @cached_property
    def lines_for_footer(self) -> list[str]:
        return AbstractDocReadMeMixin.get_lines_for_footer()

    @cached_property
    def lines(self) -> list[str]:
        return (
            [
                "# 🇱🇰 #SriLanka `Datasets`",
                "",
            ]
            + self.lines_for_global_summary
            + self.lines_for_datasets
            + ["---", ""]
            + self.lines_for_footer
        )

    def build(self) -> None:
        File(self.PATH).write_lines(self.lines)
        log.info(f"Wrote {self.PATH}")
