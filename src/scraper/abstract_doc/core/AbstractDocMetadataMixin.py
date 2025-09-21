import inspect
import os
import pathlib
from dataclasses import asdict

from utils import JSONFile, Log, TSVFile

from utils_future import FileOrDirFuture

log = Log("AbstractDocMetadataMixin")


class AbstractDocMetadataMixin:
    MAX_X_LABELS = 5

    def to_dict(self) -> dict:
        return dict(
            doc_type=self.get_doc_class_label(),
            doc_id=self.doc_id,
        ) | asdict(self)

    def write(self, force: bool = False):
        if not force and os.path.exists(self.json_path):
            return
        os.makedirs(self.dir_doc, exist_ok=True)
        JSONFile(self.json_path).write(self.to_dict())
        log.info(f"Wrote {self.json_path}")

    @classmethod
    def get_all_json_paths(cls) -> list[str]:
        return [
            str(json_path)
            for json_path in pathlib.Path(cls.get_dir_docs_for_cls()).rglob(
                "doc.json"
            )
        ]

    @classmethod
    def from_dict(cls, d: dict):
        sig = inspect.signature(cls.__init__)
        valid_keys = set(sig.parameters) - {"self"}
        filtered_data = {k: v for k, v in d.items() if k in valid_keys}
        return cls(**filtered_data)

    @classmethod
    def from_file(cls, json_path: str):
        d = JSONFile(json_path).read()
        return cls.from_dict(d)

    @classmethod
    def list_all(cls):
        doc_list = [
            cls.from_file(json_path) for json_path in cls.get_all_json_paths()
        ]
        doc_list.sort(key=lambda doc: (doc.doc_id), reverse=True)
        return doc_list

    @classmethod
    def get_url_metadata_set(cls) -> set[str]:
        return {
            doc.url_metadata
            for doc in cls.list_all()
            if doc.url_metadata is not None
        }

    @classmethod
    def get_best_time_unit(cls) -> str:
        doc_list = cls.list_all()
        for time_unit in ["decade", "year", "month", "day"]:
            ts_list = [doc.get_ts(time_unit) for doc in doc_list]
            n = len(set(ts_list))
            if n >= cls.MAX_X_LABELS:
                return time_unit
        return "year"

    def get_ts(self, time_unit: str) -> str:
        ts = {
            "decade": self.date_str[:3] + "0s",
            "year": self.date_str[:4],
            "month": self.date_str[:7],
            "day": self.date_str[:10],
        }.get(time_unit, None)
        if ts is None:
            raise ValueError(f"Invalid time_unit: {time_unit}")
        return ts

    @classmethod
    def get_ts_to_lang_to_n(cls, time_unit: str):
        idx = {}
        for doc in cls.list_all():
            ts = doc.get_ts(time_unit)
            lang = doc.lang
            if ts not in idx:
                idx[ts] = {}
            if lang not in idx[ts]:
                idx[ts][lang] = 0
            idx[ts][lang] += 1
        return idx

    @classmethod
    def get_all_tsv_path(cls, suffix) -> str:
        # E.g. "../lk_acts_data/data/lk_acts/all.tsv"
        return os.path.join(cls.get_dir_docs_for_cls(), f"docs_{suffix}.tsv")

    @classmethod
    def write_all(cls):
        d_list = [doc.to_dict() for doc in cls.list_all()]

        for n, suffix in [
            [None, "all"],
            [100, "last100"],
            [1000, "last10000"],
        ]:
            if n and n > len(d_list):
                continue

            d_list_for_file = d_list[:n] if n else d_list
            all_tsv_path = cls.get_all_tsv_path(suffix)
            TSVFile(all_tsv_path).write(d_list_for_file)
            log.info(f"Wrote {FileOrDirFuture(all_tsv_path)}")
