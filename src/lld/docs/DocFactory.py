import os
from functools import cache

from utils import JSONFile, Log

from lld.docs.abstract_doc import AbstractDoc
from lld.docs.custom_docs import Act, Bill, ExtraGazette, Gazette
from lld.docs.DocFactoryAggregated import DocFactoryAggregated

log = Log("DocFactory")


class DocFactory(DocFactoryAggregated):

    @staticmethod
    def cls_list_all():
        return [
            Gazette,
            ExtraGazette,
            Act,
            Bill,
        ]

    @staticmethod
    def cls_from_doc_type(doc_type):
        doc_type = doc_type.lower()
        for doc_cls in DocFactory.cls_list_all():
            if doc_cls.get_doc_type_name() == doc_type:
                return doc_cls
        raise ValueError(f"Unknown doc type: {doc_type}")

    @staticmethod
    def from_dict(data):
        cls = DocFactory.cls_from_doc_type(data["doc_type_name"])
        return cls.from_dict(data)

    @staticmethod
    def from_file(file_path):
        assert file_path.endswith(".json")
        data = JSONFile(file_path).read()
        return DocFactory.from_dict(data)

    @classmethod
    def __get_metadata_file_path_lists__(cls):
        file_path_lists = []
        for dir_path, _, file_names in os.walk(AbstractDoc.DIR_DATA):
            for file_name in file_names:
                if file_name == "metadata.json":
                    file_path = os.path.join(dir_path, file_name)
                    file_path_lists.append(file_path)
        return file_path_lists

    @staticmethod
    def get_total_data_size():
        total_size = 0
        for file_path in DocFactory.__get_metadata_file_path_lists__():
            total_size += os.path.getsize(file_path)
        return total_size

    @staticmethod
    @cache
    def list_all():
        doc_list = []
        for (
            metadata_file_path
        ) in DocFactory.__get_metadata_file_path_lists__():
            doc = DocFactory.from_file(metadata_file_path)
            doc_list.append(doc)

        doc_list.sort(key=lambda x: (x.date, x.doc_num), reverse=True)
        log.debug(f"Found {len(doc_list):,} docs (all types).")
        return doc_list
