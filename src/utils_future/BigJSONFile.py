import json
import math
import os
import shutil
from functools import cached_property

from utils import File, Log

log = Log("BigJSONFile")


class BigJSONFile:
    MIN_BIG_FILE_SIZE = 20_000_000

    def __init__(self, dir_path):
        self.dir_path = dir_path

    @cached_property
    def exists(self):
        return os.path.exists(self.dir_path) and os.path.isdir(self.dir_path)

    @staticmethod
    def from_json(jsoned_data: str):
        return json.loads(jsoned_data)

    @staticmethod
    def to_json(data) -> str:
        return json.dumps(data, indent=2)

    def write(self, data_list: list):
        assert isinstance(data_list, list)
        if self.exists:
            shutil.rmtree(self.dir_path)
        os.makedirs(self.dir_path, exist_ok=True)

        content = json.dumps(data_list, indent=2)
        total_size = len(content)
        n_chunks = math.ceil(total_size / self.MIN_BIG_FILE_SIZE)
        n_data_list = len(data_list)
        log.debug(f"{n_data_list=:,}, {total_size=:,}, {n_chunks=:,}")

        for i in range(n_chunks):
            chunk_path = os.path.join(self.dir_path, f"part_{i + 1:04d}")
            i_start = i * self.MIN_BIG_FILE_SIZE
            i_end = min((i + 1) * self.MIN_BIG_FILE_SIZE, total_size)
            chunk_content = content[i_start:i_end]
            File(chunk_path).write(chunk_content)
            chunk_size_m = os.path.getsize(chunk_path) / 1_000_000
            log.debug(f"Wrote {chunk_path} ({chunk_size_m:.1f} MB)")

    def read(self) -> list:
        if not self.exists:
            return []
        content_list = []
        for chunk_file in sorted(os.listdir(self.dir_path)):
            chunk_path = os.path.join(self.dir_path, chunk_file)
            chunk_content = File(chunk_path).read()
            content_list.append(chunk_content)
        content = "".join(content_list)
        return json.loads(content)
