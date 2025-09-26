import requests
from utils import Log

log = Log("GlobalReadMeSummaryMixin")


class GlobalReadMeSummaryMixin:

    @classmethod
    def get_url_summary(cls, repo_name: str, doc_class_label: str) -> str:
        is_multi_doc = repo_name != doc_class_label
        branch_name = f"data_{doc_class_label}" if is_multi_doc else "data"
        return "/".join(
            [
                "https://raw.githubusercontent.com",
                "nuuuwan",
                repo_name,
                "refs",
                "heads",
                branch_name,
                "data",
                doc_class_label,
                "summary.json",
            ]
        )

    @classmethod
    def get_summary(cls, repo_name, doc_class_label):
        try:
            url = cls.get_url_summary(repo_name, doc_class_label)
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log.error(
                f"Failed to get summary for {repo_name}/{doc_class_label}: {e}"
            )
            return None

    def get_summary_list(self) -> list[dict]:
        summary_list = []
        for repo_name, doc_class_labels in self.repo_to_doc_classes.items():
            for doc_class_label in doc_class_labels:
                summary = self.get_summary(repo_name, doc_class_label)
                if summary:
                    summary_list.append(summary)
        return summary_list

    @classmethod
    def get_global_summary(cls, summary_list) -> dict:
        return dict(
            n_datasets=len(summary_list),
            n_docs=sum([s.get("n_docs", 0) for s in summary_list]),
            all_dataset_size=sum(
                [s.get("dataset_size", 0) for s in summary_list]
            ),
        )
