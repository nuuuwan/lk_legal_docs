import os
from functools import cache

from utils import JSONFile, Log

from lld.docs.abstract_doc import AbstractDoc
from lld.docs.custom_docs import Act, Bill, ExtraGazette, Gazette
from utils_future import Directory

log = Log("DocFactory")


class DocFactory:
    DOCS_ALL_JSON_PATH = os.path.join(AbstractDoc.DIR_DATA, "all.json")
    N_LATEST = 100

    DOCS_LATEST_JSON_PATH = os.path.join(
        AbstractDoc.DIR_DATA, f"latest-{N_LATEST}.json"
    )
    DOCS_TEMP_DATA_SUMMARY_JSON_PATH = os.path.join(
        AbstractDoc.DIR_TEMP_DATA, "temp_data_summary.json"
    )

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

    @staticmethod
    def x_to_list_all(doc_list, func_get_key):
        doc_type_dict = {}
        for doc in doc_list:
            key = func_get_key(doc)
            if key not in doc_type_dict:
                doc_type_dict[key] = []
            doc_type_dict[key].append(doc)
        return doc_type_dict

    @staticmethod
    def get_total_data_size():
        return Directory(AbstractDoc.DIR_DATA).size

    @staticmethod
    def write_all():
        doc_list = DocFactory.list_all()
        data_list = [doc.to_minimal_dict() for doc in doc_list]

        for json_file_path, n in [
            (DocFactory.DOCS_ALL_JSON_PATH, len(data_list)),
            (
                DocFactory.DOCS_LATEST_JSON_PATH,
                min(DocFactory.N_LATEST, len(data_list)),
            ),
        ]:
            JSONFile(json_file_path).write(data_list[:n])
            file_size_k = os.path.getsize(json_file_path) / 1000
            log.debug(f"Wrote {json_file_path} ({file_size_k:,.0f} KB)")

    @staticmethod
    def get_temp_data_summary():
        doc_list = DocFactory.list_all()
        temp_data_summary = dict(
            n_docs=len(doc_list),
            n_docs_with_pdfs=len([d for d in doc_list if d.n_pdfs > 0]),
            n_pdfs=sum(d.n_pdfs for d in doc_list),
            total_file_size=Directory(AbstractDoc.DIR_TEMP_DATA).size,
        )
        log.debug(f"{temp_data_summary=}")
        return temp_data_summary

    @staticmethod
    def write_temp_data_summary():
        temp_data_summary = DocFactory.get_temp_data_summary()
        json_file_path = DocFactory.DOCS_TEMP_DATA_SUMMARY_JSON_PATH
        JSONFile(json_file_path).write(temp_data_summary)
        log.debug(f"Wrote {json_file_path} ({temp_data_summary})")
