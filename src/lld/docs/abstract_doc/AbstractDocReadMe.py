import os

from utils import File

from lld.docs.abstract_doc.AbstractDoc import log


class AbstractDocReadMe:

    @property
    def readme_lines(self):
        return [
            f"# [{self.doc_num}] {self.description}",
            "",
            f"**Date:** {self.date}",
            "",
            "## Original Sources",
            "",
            f"- [English]({self.source_url_en})",
            f"- [Sinhala]({self.source_url_si})",
            f"- [Tamil]({self.source_url_ta})",
        ]

    def write_readme(self):
        readme_path = os.path.join(self.dir_data, "README.md")
        File(readme_path).write_lines(self.readme_lines)
        log.debug(f"Wrote {readme_path}")
