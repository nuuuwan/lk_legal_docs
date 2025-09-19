import json
import math
import os
from functools import cached_property

from utils import Log

log = Log("BigJSONFile")


class BigJSONFile:
    MIN_BIG_FILE_SIZE = 50_000_000

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
        if not self.exists:
            os.makedirs(self.dir_path, exist_ok=True)
        total_size = len(BigJSONFile.to_json(data_list))
        n_chunks = int(math.ceil(total_size / self.MIN_BIG_FILE_SIZE))
        n_per_chunk = int(math.ceil(len(data_list) / n_chunks))

        for i_chunk in range(n_chunks):
            chunk_path = os.path.join(
                self.dir_path, f"part-{i_chunk:03d}.json"
            )
            i_start = i_chunk * n_per_chunk
            i_end = min(i_start + n_per_chunk, len(data_list))
            chunk_data = data_list[i_start:i_end]
            with open(chunk_path, "w", encoding="utf-8") as f:
                f.write(BigJSONFile.to_json(chunk_data))
            chunk_size_m = os.path.getsize(chunk_path) / 1_000_000
            log.debug(f"Wrote {chunk_path} ({chunk_size_m:.1f} MB)")
        total_size_m = total_size / 1_000_000
        log.info(f"Wrote {self.dir_path} ({total_size_m:.1f} MB)")

    def __get_chunk_paths__(self) -> list:
        if not self.exists:
            return []
        chunk_paths = []
        for file_name in os.listdir(self.dir_path):
            if file_name.startswith("part-") and file_name.endswith(".json"):
                chunk_paths.append(os.path.join(self.dir_path, file_name))
        chunk_paths.sort()
        return chunk_paths

    def read(self) -> list:
        data_list = []
        for chunk_path in self.__get_chunk_paths__():
            with open(chunk_path, "r", encoding="utf-8") as f:
                chunk_data = BigJSONFile.from_json(f.read())
                assert isinstance(chunk_data, list)
                data_list.extend(chunk_data)
            chunk_size_m = os.path.getsize(chunk_path) / 1_000_000
            log.debug(f"Read {chunk_path} ({chunk_size_m:.1f} MB)")
        total_size = len(BigJSONFile.to_json(data_list))
        total_size_m = total_size / 1_000_000
        log.info(f"Read {self.dir_path} ({total_size_m:.1f} MB)")
        return data_list
