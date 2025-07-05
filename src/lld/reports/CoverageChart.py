import os
from functools import cached_property

import matplotlib.pyplot as plt
from utils import Log

from lld.docs import DocFactory

log = Log("CoverageChart")


class CoverageChart:
    IMAGE_PATH = os.path.join("images", "coverage_chart.png")

    def __init__(self):
        self.doc_list = DocFactory.list_all()

    @cached_property
    def date_to_type_to_n(self):
        idx = {}
        for doc in self.doc_list:
            t = doc.year_and_month
            doc_type = doc.get_doc_type_name()

            if t not in idx:
                idx[t] = {}

            if doc_type not in idx[t]:
                idx[t][doc_type] = 0

            idx[t][doc_type] += 1

        return idx

    def draw_chart(self):
        date_to_type_to_n = self.date_to_type_to_n
        dates = sorted(date_to_type_to_n.keys())

        all_types = sorted(
            set(t for d in date_to_type_to_n.values() for t in d)
        )

        type_to_counts = {t: [] for t in all_types}
        for date in dates:
            for t in all_types:
                type_to_counts[t].append(date_to_type_to_n[date].get(t, 0))

        # Plot
        fig, ax = plt.subplots(
            figsize=(16, 9)
        )  # Set figure size to 16x9 inches

        bottom = [0] * len(dates)
        for t in all_types:
            ax.bar(dates, type_to_counts[t], bottom=bottom, label=t)
            bottom = [b + c for b, c in zip(bottom, type_to_counts[t])]

        ax.set_xlabel("Date")
        ax.set_ylabel("Document Count")
        ax.set_title("Documents over Time")
        ax.legend(title="Document Type")
        plt.xticks(rotation=45)
        plt.tight_layout()

        os.makedirs(os.path.dirname(self.IMAGE_PATH), exist_ok=True)
        plt.savefig(self.IMAGE_PATH, dpi=300)
        plt.close()
        log.info(f"Wrote {self.IMAGE_PATH}.")
        return self.IMAGE_PATH
