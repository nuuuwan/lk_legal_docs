import os
from functools import cached_property

from utils import File, Log

log = Log("AbstractDocTextMixin")


class AbstractDocTextMixin:

    @cached_property
    def text_path(self) -> str:
        return os.path.join(self.dir_doc, "doc.txt")

    @property
    def has_text(self) -> bool:
        return os.path.exists(self.text_path)

    @cached_property
    def doc_readme_path(self) -> str:
        return os.path.join(self.dir_doc, "README.md")

    def extract_text(self):
        content = self.description
        File(self.text_path).write(content)
        log.info(f"Wrote {self.text_path}")

    def get_text(self):
        if not os.path.exists(self.text_path):
            return ""
        return File(self.text_path).read()
