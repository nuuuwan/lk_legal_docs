import os

import matplotlib.pyplot as plt
import numpy as np
from utils import Log

log = Log("AbstractDocChartDocsByYearMixin")


class AbstractDocChartDocsByYearMixin:
    LANGS = ["si", "ta", "en"]
    COLOR_MAP = {
        "si": "#8D153A",
        "ta": "#EB7400",
        "en": "#00534E",
    }

    @classmethod
    def get_chart_image_name(cls) -> str:
        return "docs_by_year_and_lang.png"

    @classmethod
    def get_chart_image_path(cls) -> str:
        # E.g. ../lk_acts_data/data/lk_acts/docs_by_year_and_lang.png
        return os.path.join(
            cls.get_dir_docs_for_cls(), cls.get_chart_image_name()
        )

    @classmethod
    def build_chart_by_year_and_lang(cls, year_to_lang_to_n):

        years = sorted(year_to_lang_to_n.keys())
        langs = sorted(
            {lang for v in year_to_lang_to_n.values() for lang in v.keys()}
        )

        counts = {
            lang: [
                year_to_lang_to_n.get(year, {}).get(lang, 0) for year in years
            ]
            for lang in langs
        }

        _, ax = plt.subplots(figsize=(10, 6))
        bottom = np.zeros(len(years))

        for lang in cls.LANGS:
            color = cls.COLOR_MAP.get(lang, "grey")
            values = counts.get(lang, 0)
            ax.bar(years, values, bottom=bottom, label=lang, color=color)
            bottom += np.array(values)

        ax.set_xlabel("Year")
        ax.set_ylabel("Number of documents")
        ax.set_title(
            f"Number of {cls.get_doc_class_label()} by year & language"
        )
        ax.set_xticks(years)
        ax.legend(title="Language")
        plt.tight_layout()

        image_path = cls.get_chart_image_path()
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f"Wrote {image_path}")
