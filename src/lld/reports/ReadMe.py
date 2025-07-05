from utils import File, Log, Time, TimeFormat

from lld.docs import DocFactory

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    def __init__(self):
        self.time_str = TimeFormat.TIME.format(Time.now())

    @staticmethod
    def get_metadata_md(metadata):
        return (
            f"- [{metadata.doc_num}] "
            + f"[{metadata.description}]({metadata.dir_data})"
        )

    @staticmethod
    def get_lines_for_doc(doc_cls):
        metadata_list = doc_cls.list_all()
        n = len(metadata_list)
        return (
            [
                f"## {doc_cls.get_doc_type_name().title()} ({n:,})",
                "",
            ]
            + [ReadMe.get_metadata_md(metadata) for metadata in metadata_list]
            + [""]
        )

    def get_lines_for_docs(self):
        lines = []
        for doc_cls in DocFactory.list_all_cls():
            lines.extend(self.get_lines_for_doc(doc_cls))
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
