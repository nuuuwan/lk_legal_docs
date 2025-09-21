import json
import os

from utils import File, Log

from utils_future import FileOrDirFuture, Format

log = Log("AbstractDocReadMeMixin")


class AbstractDocReadMeMixin:
    N_LATEST = 20

    @classmethod
    def get_lines_for_header(cls, summary) -> list[str]:
        title = Format.title(
            summary["doc_class_emoji"] + summary["doc_class_label"]
        )
        return [
            f"# {title} `Dataset`",
            "",
        ]

    @classmethod
    def get_line_for_blurb_item_files(cls, summary) -> list[str]:
        n_docs = summary["n_docs"]
        n_docs_with_pdfs = summary["n_docs_with_pdfs"]
        n_docs_with_text = summary["n_docs_with_text"]

        blob_list = []
        for doc_type, n in [
            ("JSON", n_docs),
            ("PDF", n_docs_with_pdfs),
            ("TXT", n_docs_with_text),
            ("🤗 Hugging Face", n_docs_with_text),
            ("Something New", 0),
        ]:
            if n == 0:
                continue
            p = n / n_docs

            label = "" if (n == n_docs) else f"({p:.0%})"
            blob_list.append(f"**{doc_type}** {label}".strip())
        return "- In " + Format.and_list(blob_list)

    @classmethod
    def get_line_for_blurb_item_lang(cls, summary) -> list[str]:
        langs = summary["langs"]
        blurb_langs = []
        for lang_i, lang_label in [
            ["si", "සිංහල"],
            ["ta", "தமிழ்"],
            ["en", "English"],
        ]:
            for lang in langs:
                if lang_i in lang:
                    blurb_langs.append(f"**{lang_label}**")
                    break

        return "- In " + Format.and_list(blurb_langs)

    @classmethod
    def get_lines_for_blurb(cls, summary) -> list[str]:
        doc_class_description = summary["doc_class_description"]
        time_updated = summary["time_updated"]
        n_docs = summary["n_docs"]
        date_str_min = summary["date_str_min"]
        date_str_max = summary["date_str_max"]
        dataset_size = summary["dataset_size"]
        url_source = summary["url_source"]
        url_data = summary["url_data"]

        dataset_size_humanized = FileOrDirFuture.humanize_size(dataset_size)
        time_updated_for_badge = Format.badge(time_updated)

        return [
            "![LastUpdated](https://img.shields.io/badge"
            + f"/last_updated-{time_updated_for_badge}-green)",
            "",
            f"[{url_data}]({url_data})",
            "",
            doc_class_description,
            "",
            f"- [**{n_docs:,}** documents]({url_data})"
            + f" (**{dataset_size_humanized}**),"
            + f" from **{date_str_min}** to **{date_str_max}**,"
            + f" scraped from **[{url_source}]({url_source})**",
            "",
            cls.get_line_for_blurb_item_files(summary),
            "",
            cls.get_line_for_blurb_item_lang(summary),
            "",
        ]

    @classmethod
    def get_lines_for_metadata_example(cls, summary) -> list[str]:
        latest_doc_d = summary["latest_doc_d"]
        return [
            "## 📝 Example Metadata",
            "",
            "```json",
            json.dumps(latest_doc_d, indent=4),
            "```",
            "",
        ]

    @classmethod
    def get_lines_chart_docs_by_year_and_lang(cls, summary) -> list[str]:
        url_chart = summary["url_chart"]
        return [
            f"![Chart]({url_chart})",
            "",
        ]

    @classmethod
    def get_lines_for_hugging_face(cls):
        url_hf = (
            "https://img.shields.io/badge"
            + "/-HuggingFace-FDEE21"
            + "?style=for-the-badge&logo=HuggingFace"
        )
        lines = [
            "## 🤗 Hugging Face Datasets",
            "",
            f"![HuggingFace]({url_hf})",
            "",
        ]

        for label_suffix in ["docs", "chunks"]:
            dataset_id = cls.get_dataset_id(label_suffix)
            url = cls.get_dataset_url(label_suffix)
            lines.append(f"- [{dataset_id}]({url})")
        lines.append("")
        return lines

    @classmethod
    def get_lines_for_latest_docs(cls):
        lines = [f"## 🆕 {cls.N_LATEST} Latest documents", ""]
        for doc in cls.list_all()[: cls.N_LATEST]:
            line = "- " + " | ".join(
                [
                    doc.date_str,
                    f"`{doc.num}`",
                    doc.description,
                    f"[data]({doc.remote_data_url})",
                ]
            )
            lines.append(line)
        lines.append("")
        return lines

    @classmethod
    def get_lines_for_more_datasets(cls) -> list[str]:
        return [
            "---",
            "",
            "### [More Datasets about 🇱🇰 #SriLanka]"
            + "(https://github.com/nuuuwan/lk_datasets)",
            "",
        ]

    @classmethod
    def get_lines_for_footer(cls) -> list[str]:
        return [
            "![Maintainer]"
            + "(https://img.shields.io/badge/maintainer-nuuuwan-red)",
            "![MadeWith](https://img.shields.io/badge/made_with-python-blue)",
            "[![License: MIT]"
            + "(https://img.shields.io/badge/License-MIT-yellow.svg)]"
            + "(https://opensource.org/licenses/MIT)",
            "",
        ]

    @classmethod
    def lines(cls) -> list[str]:
        summary = cls.get_summary()
        return (
            cls.get_lines_for_header(summary)
            + cls.get_lines_for_blurb(summary)
            + cls.get_lines_for_metadata_example(summary)
            + cls.get_lines_chart_docs_by_year_and_lang(summary)
            + cls.get_lines_for_hugging_face()
            + cls.get_lines_for_latest_docs()
            + cls.get_lines_for_more_datasets()
            + cls.get_lines_for_footer()
        )

    @classmethod
    def get_doc_class_readme_path(cls) -> str:
        # E.g. ../lk_acts_data/data/lk_acts/README.md
        return os.path.join(cls.get_dir_docs_for_cls(), "README.md")

    @classmethod
    def build_doc_class_readme(cls):
        assert cls.list_all()
        os.makedirs(cls.get_main_branch_dir_root(), exist_ok=True)
        readme_path = cls.get_doc_class_readme_path()
        File(readme_path).write("\n".join(cls.lines()))
        log.info(f"Wrote {readme_path}")
