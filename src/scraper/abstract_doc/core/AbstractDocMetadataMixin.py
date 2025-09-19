import inspect
import os
import pathlib
from dataclasses import asdict

from utils import JSONFile, Log

log = Log("AbstractDocMetadataMixin")


class AbstractDocMetadataMixin:

    def to_dict(self) -> dict:
        return dict(
            doc_type=self.get_doc_class_label(),
            doc_id=self.doc_id,
        ) | asdict(self)

    def write(self):
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
    def get_year_to_n(cls):
        year_to_n = {}
        for doc in cls.list_all():
            year_to_n[doc.year] = year_to_n.get(doc.year, 0) + 1
        year_to_n = dict(sorted(year_to_n.items(), key=lambda x: x[0]))
        return year_to_n
