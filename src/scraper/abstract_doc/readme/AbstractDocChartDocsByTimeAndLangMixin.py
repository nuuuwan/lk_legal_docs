import os

import matplotlib.pyplot as plt
import numpy as np
from utils import Log

log = Log("AbstractDocChartDocsByTimeAndLangMixin")


class AbstractDocChartDocsByTimeAndLangMixin:
    LANGS = ["si", "ta", "en"]
    COLOR_MAP = {
        "si": "#8D153A",
        "ta": "#EB7400",
        "en": "#00534E",
        "si-ta-en": "#FFBE29",
    }

    @classmethod
    def get_chart_image_name(cls, time_unit) -> str:
        return f"docs_by_{time_unit}_and_lang.png"

    @classmethod
    def get_chart_image_path(cls, time_unit) -> str:
        # E.g. ../lk_acts_data/data/lk_acts/docs_by_year_and_lang.png
        return os.path.join(
            cls.get_dir_docs_for_cls(), cls.get_chart_image_name(time_unit)
        )

    @classmethod
    def get_raw_remote_chart_image_url(cls, time_unit) -> str:
        # E.g. https://raw.githubusercontent.com/nuuuwan/lk_appeal_court_judgements/refs/heads/data/data/lk_appeal_court_judgements/docs_by_year_and_lang.png # noqa: E501
        return "/".join(
            [
                cls.get_raw_remote_data_branch_url(),
                cls.get_dir_docs_for_cls_relative(),
                cls.get_chart_image_name(time_unit),
            ]
        )

    @classmethod
    def __prepare_chart_data__(cls, ts_to_lang_n: dict):
        ts = sorted(ts_to_lang_n.keys())
        langs = sorted(
            {lang for v in ts_to_lang_n.values() for lang in v.keys()}
        )
        counts = {
            lang: [ts_to_lang_n.get(year, {}).get(lang, 0) for year in ts]
            for lang in langs
        }
        return ts, langs, counts

    @classmethod
    def __plot_stacked_bars__(cls, ax, ts_list, counts):
        bottom = np.zeros(len(ts_list))
        for lang in cls.LANGS:
            values = counts.get(lang, [])
            if values:
                color = cls.COLOR_MAP.get(lang, "grey")
                ax.bar(
                    ts_list, values, bottom=bottom, label=lang, color=color
                )
                bottom += np.array(values)
        return bottom

    @staticmethod
    def __compute_xticks__(ts_list: list[int]) -> list[int]:
        if len(ts_list) <= 5:
            return ts_list
        step = max(1, len(ts_list) // 5)
        xticks = ts_list[::step]
        if xticks[-1] != ts_list[-1]:
            xticks.append(ts_list[-1])
        return xticks

    @classmethod
    def __configure_axes__(cls, ax, ts_list, time_unit):
        x_label = time_unit.title()
        ax.set_xlabel(x_label)
        ax.set_ylabel("Number of documents")
        ax.set_title(
            f"Number of {cls.get_doc_class_label()} by {x_label} & Language"
        )
        xticks = cls.__compute_xticks__(ts_list)
        ax.set_xticks(xticks)
        ax.set_xticklabels([str(y) for y in xticks], rotation=45)
        ax.legend(title="Language")
        plt.tight_layout()

    @classmethod
    def __save_chart__(cls, fig, time_unit):
        image_path = cls.get_chart_image_path(time_unit)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        fig.savefig(image_path, dpi=300)
        plt.close(fig)
        log.info(f"Wrote {image_path}")

    @classmethod
    def build_chart_by_time_and_lang(cls, ts_to_lang_n: dict, time_unit):
        ts_list, _, counts = cls.__prepare_chart_data__(ts_to_lang_n)
        fig, ax = plt.subplots(figsize=(8, 4.5))
        cls.__plot_stacked_bars__(ax, ts_list, counts)
        cls.__configure_axes__(ax, ts_list, time_unit)
        cls.__save_chart__(fig, time_unit)
