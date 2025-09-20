import os

from utils import JSONFile, Log, Time, TimeFormat

from utils_future import FileOrDirFuture

log = Log("AbstractDocSummaryMixin")


class AbstractDocSummaryMixin:

    @property
    def has_pdf(self) -> bool:
        return False

    @classmethod
    def get_summary(cls) -> dict:
        doc_list = cls.list_all()
        doc_class_label = cls.get_doc_class_label()
        doc_class_emoji = cls.get_doc_class_emoji()
        doc_class_description = cls.get_doc_class_description()
        time_updated = TimeFormat.TIME.format(Time.now())
        n_docs = len(doc_list)
        n_docs_with_pdfs = len([doc for doc in doc_list if doc.has_pdf])
        n_docs_with_text = len([doc for doc in doc_list if doc.has_text])
        date_strs = [doc.date_str for doc in doc_list]
        date_str_min = min(date_strs)
        date_str_max = max(date_strs)
        dataset_size = FileOrDirFuture(cls.get_data_branch_dir_root()).size
        latest_doc = doc_list[0]
        url_source = latest_doc.url_metadata.split("?")[0]
        url_data = cls.get_remote_data_url_for_class()
        latest_doc_d = latest_doc.to_dict()
        langs = set([doc.lang for doc in doc_list])
        year_to_lang_to_n = cls.get_year_to_lang_to_n()

        return dict(
            doc_class_label=doc_class_label,
            doc_class_emoji=doc_class_emoji,
            doc_class_description=doc_class_description,
            time_updated=time_updated,
            n_docs=n_docs,
            n_docs_with_pdfs=n_docs_with_pdfs,
            n_docs_with_text=n_docs_with_text,
            date_str_min=date_str_min,
            date_str_max=date_str_max,
            dataset_size=dataset_size,
            url_source=url_source,
            url_data=url_data,
            langs=list(langs),
            latest_doc_d=latest_doc_d,
            year_to_lang_to_n=year_to_lang_to_n,
        )

    @classmethod
    def get_summary_path(cls) -> str:
        # E.g. ../lk_acts_data/data/lk_acts/summary.json
        return os.path.join(cls.get_dir_docs_for_cls(), "summary.json")

    @classmethod
    def build_summary(cls):
        summary = cls.get_summary()
        log.debug(f"{summary=}")
        summary_json_path = cls.get_summary_path()
        os.makedirs(cls.get_main_branch_dir_root(), exist_ok=True)
        JSONFile(summary_json_path).write(summary)
        log.info(f"Wrote {summary_json_path}")
