import os

from utils import Log

from lld.docs.custom_docs import Act, Bill, ExtraGazette

log = Log("DocFactory")


class DocFactory:
    @staticmethod
    def list_all_cls():
        return [
            # Act,
            # Bill,
            ExtraGazette,
        ]

    @staticmethod
    def list_all():
        doc_list = []
        for doc_cls in DocFactory.list_all_cls():
            doc_list.extend(doc_cls.list_all())

        doc_list.sort(key=lambda x: (x.date, x.doc_num), reverse=True)
        log.debug(f"Found {len(doc_list):,} docs.")
        return doc_list

    @staticmethod
    def get_total_data_size():
        total_size = 0
        root_path = "data"
        for dirpath, _, filenames in os.walk(root_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size
