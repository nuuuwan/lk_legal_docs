import json

from utils import File, Log, Time, TimeFormat

from lld.docs import DocFactory

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"
    N_DISPLAY_DOCS = 1_000

    def __init__(self):
        self.time_str = TimeFormat.TIME.format(Time.now())
        self.doc_list = DocFactory.list_all()
        self.total_data_size_m = DocFactory.get_total_data_size() / 1_000_000.0

    @staticmethod
    def get_doc_md_lines(doc):
        doc_cls = doc.__class__
        return [
            (
                f"- {doc_cls.get_emoji()} {doc.date}"
                + f" [{doc.description}]({doc.dir_data})"
                + f" [{doc.doc_num}]"
            )
        ]

    def get_doc_legend(self):
        doc_cls_list = DocFactory.list_all_cls()
        inner = ", ".join(
            f"{doc_cls.get_emoji()} = {doc_cls.get_doc_type_name().title()}"
            for doc_cls in doc_cls_list
        )
        return f"({inner})"

    def get_lines_for_docs(self):

        lines = ["## Documents (Latest)", "", self.get_doc_legend()]
        previous_year = None
        previous_year_and_month = None
        for doc in self.doc_list:
            year = doc.year
            year_and_month = doc.year_and_month
            if year != previous_year:
                lines.extend(["", f"### {year}"])
                previous_year = year
            if year_and_month != previous_year_and_month:
                lines.extend(["", f"#### {year_and_month}", ""])
                previous_year_and_month = year_and_month

            lines.extend(self.get_doc_md_lines(doc))
        return lines

    def get_lines_metadata(self):
        latest_doc = self.doc_list[0]
        return [
            "## Metadata Example",
            "",
            "```json",
            json.dumps(latest_doc.__dict__, indent=4),
            "```",
            "",
        ]

    @property
    def lines(self):
        n = len(self.doc_list)
        return (
            [
                "# Legal Documents - #SriLanka 🇱🇰",
                "",
                f"**{n:,}** documents (**{self.total_data_size_m:,.0f}MB**)"
                + f" as of **{self.time_str}**.",
                "",
                "A collection of"
                + " Legal Gazettes, Extra Gazettes, Acts, Bills and more, scraped"
                + " from [documents.gov.lk](https://documents.gov.lk).",
                "",
                "🆓 **Public** data, fully open-source – fork freely!",
                "",
                "🗣️ **Tri-Lingual** - සිංහල, தமிழ் & English",
                "",
                "🔍 **Useful** for Journalists, Researchers,"
                + " Lawyers & law students,"
                + " Policy watchers & Citizens who want to stay informed",
                "",
                "#SriLanka #Legal #OpenData #GovTech",
                "",
            ]
            + self.get_lines_metadata()
            + self.get_lines_for_docs()
        )

    def build(self):
        File(self.PATH).write("\n".join(self.lines))
        log.debug(f"Wrote {len(self.lines)} lines to {self.PATH}.")
