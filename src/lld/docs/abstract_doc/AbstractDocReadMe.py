import os

from utils import File, Log

log = Log("AbstractDocReadMe")


class AbstractDocReadMe:

    @property
    def readme_lines(self):

        source_lines = []
        for lang_str, source_url in [
            ("සිංහල", self.source_url_si),
            ("தமிழ்", self.source_url_ta),
            ("English", self.source_url_en),
        ]:
            if source_url:
                source_lines.append(f"- [{lang_str}]({source_url})")

        return (
            [
                f"# [{self.doc_num}] {self.description}",
                "",
                f"**Date:** {self.date}",
                "",
                "## Original Sources",
                "",
            ]
            + source_lines
            + [""]
        )

    def write_readme(self, force=False):
        readme_path = os.path.join(self.dir_data, "README.md")
        if not force and os.path.exists(readme_path):
            return
        File(readme_path).write_lines(self.readme_lines)
        log.debug(f"Wrote {readme_path}")
