import os
from functools import cached_property

from utils import File


class FileOrDirFuture(File):

    def __str__(self):
        return f"{self.path} ({self.size_humanized})"

    def __hash__(self):
        return hash(self.path)

    @cached_property
    def exists(self):
        return os.path.exists(self.path)

    @cached_property
    def is_dir(self):
        return os.path.isdir(self.path)

    @cached_property
    def size(self):
        if not self.exists:
            return 0

        if os.path.isfile(self.path):
            return os.path.getsize(self.path)

        total = 0
        for root, _, files in os.walk(self.path):
            for f in files:
                total += os.path.getsize(os.path.join(root, f))

        return total

    @staticmethod
    def humanize_size(size):
        for unit, label in [
            (1_000_000_000, "GB"),
            (1_000_000, "MB"),
            (1_000, "kB"),
        ]:
            if size >= unit:
                return f"{size / unit:.1f} {label}"
        return f"{size} B"

    @cached_property
    def size_humanized(self):
        return FileOrDirFuture.humanize_size(self.size)
