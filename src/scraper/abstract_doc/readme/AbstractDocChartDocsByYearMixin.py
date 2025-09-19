import os

import matplotlib.pyplot as plt
from utils import Log

log = Log("AbstractDocChartDocsByYearMixin")


class AbstractDocChartDocsByYearMixin:

    @classmethod
    def get_chart_image_path(cls) -> str:
        # E.g. ../lk_acts_data/data/lk_acts/docs_by_year.png
        return os.path.join(cls.get_dir_docs_for_cls(), "docs_by_year.png")

    @classmethod
    def get_chart_build(cls):
        year_to_n = cls.get_year_to_n()
        years = list(year_to_n.keys())
        ns = list(year_to_n.values())

        _, ax = plt.subplots(figsize=(10, 6))
        ax.bar(years, ns)
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of documents")
        ax.set_title(f"Number of {cls.get_doc_class_label()}" + " by year")
        ax.set_xticks(years)
        plt.tight_layout()

        image_path = cls.get_chart_image_path()
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f"Wrote {image_path}")
