from utils import File, Log, Time, TimeFormat

from lld.docs import DocFactory

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    def __init__(self):
        self.time_str = TimeFormat.TIME.format(Time.now())

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

    def get_lines_for_docs(self):
        doc_list = DocFactory.list_all()
        n = len(doc_list)
        lines = [f"## Documents ({n:,})", ""]
        for doc in doc_list:
            lines.extend(self.get_doc_md_lines(doc))
        return lines

    @property
    def lines(self):
        return [
            "# Legal Documents - #SriLanka 🇱🇰",
            "",
            f"*Last updated {self.time_str}*.",
            "",
            "Legal Gazettes, Extra-Gazettes, Acts, Bills"
            + " and other documents scraped"
            + " from [documents.gov.lk](https://documents.gov.lk).",
            "",
        ] + self.get_lines_for_docs()

    def build(self):
        File(self.PATH).write("\n".join(self.lines))
        log.debug(f"Wrote {len(self.lines)} lines to {self.PATH}.")
