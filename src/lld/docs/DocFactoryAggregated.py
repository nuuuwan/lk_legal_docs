import os

from utils import JSONFile, Log

from lld.docs.abstract_doc import AbstractDoc
from utils_future import Directory

log = Log("DocFactoryAggregated")


class DocFactoryAggregated:
    N_LATEST = 100
    DOCS_ALL_JSON_PATH = os.path.join(AbstractDoc.DIR_TEMP_DATA, "all.json")
    DOCS_LATEST_JSON_PATH = os.path.join(
        AbstractDoc.DIR_TEMP_DATA, f"latest-{N_LATEST}.json"
    )
    DOCS_TEMP_DATA_SUMMARY_JSON_PATH = os.path.join(
        AbstractDoc.DIR_TEMP_DATA, "temp_data_summary.json"
    )
    LEGACY_DOCS_TEMP_DATA_SUMMARY_JSON_PATH = os.path.join(
        AbstractDoc.DIR_TEMP_DATA, "data", "temp_data_summary.json"
    )

    @classmethod
    def list_all_for_decade(cls, decade):
        doc_list = cls.list_all()
        return [doc for doc in doc_list if doc.decade == decade]

    @classmethod
    def write_all(cls, decade):
        doc_list = cls.list_all_for_decade(decade)
        data_list = [doc.to_minimal_dict() for doc in doc_list]

        for json_file_path, n in [
            (cls.DOCS_ALL_JSON_PATH, len(data_list)),
            (
                cls.DOCS_LATEST_JSON_PATH,
                min(cls.N_LATEST, len(data_list)),
            ),
        ]:
            JSONFile(json_file_path).write(data_list[:n])
            file_size_k = os.path.getsize(json_file_path) / 1000
            log.debug(f"Wrote {json_file_path} ({file_size_k:,.0f} KB)")

    @classmethod
    def get_temp_data_summary(cls, decade):
        doc_list = cls.list_all_for_decade(decade)
        temp_data_summary = dict(
            n_docs=len(doc_list),
            n_docs_with_pdfs=len([d for d in doc_list if d.n_pdfs > 0]),
            n_docs_with_pdfs_fail=len(
                [d for d in doc_list if d.n_pdfs_fail > 0]
            ),
            n_pdfs=sum(d.n_pdfs for d in doc_list),
            total_file_size=Directory(AbstractDoc.DIR_TEMP_DATA).size,
        )
        log.debug(f"{temp_data_summary=}")
        return temp_data_summary

    @classmethod
    def write_temp_data_summary(cls, decade):
        temp_data_summary = cls.get_temp_data_summary(decade)
        json_file_path = cls.DOCS_TEMP_DATA_SUMMARY_JSON_PATH
        JSONFile(json_file_path).write(temp_data_summary)
        log.debug(f"Wrote {json_file_path} ({temp_data_summary})")

        if os.path.exists(cls.LEGACY_DOCS_TEMP_DATA_SUMMARY_JSON_PATH):
            os.remove(cls.LEGACY_DOCS_TEMP_DATA_SUMMARY_JSON_PATH)
