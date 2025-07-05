import os

from utils import JSONFile, Log

log = Log("AbstractDocSerializer")


class AbstractDocSerializer:

    @classmethod
    def from_dict(cls, data):
        return cls(
            doc_num=data["doc_num"],
            date=data["date"],
            description=data["description"],
            source_url_en=data["source_url_en"],
            source_url_si=data["source_url_si"],
            source_url_ta=data["source_url_ta"],
        )

    @classmethod
    def from_file(cls, file_path):
        data = JSONFile(file_path).read()
        return cls.from_dict(data)

    @classmethod
    def __get_doc_file_path_lists__(cls):
        file_path_lists = []
        for year in os.listdir(cls.get_doc_type_dir()):
            dir_data_for_year = os.path.join(cls.get_doc_type_dir(), year)
            for id in os.listdir(dir_data_for_year):
                dir_data = os.path.join(dir_data_for_year, id)
                file_path = os.path.join(dir_data, "metadata.json")
                if not os.path.exists(file_path):
                    log.warning(f"{file_path} not found.")
                    continue
                file_path_lists.append(file_path)
        return file_path_lists

    @classmethod
    def list_all(cls):
        doc_file_path_lists = cls.__get_doc_file_path_lists__()
        doc_doc_list = [
            cls.from_file(file_path) for file_path in doc_file_path_lists
        ]
        doc_doc_list.sort(key=lambda x: x.id, reverse=True)
        log.info(f"Found {len(doc_doc_list):,} docs.")
        return doc_doc_list

    def write(self):
        file_path = os.path.join(self.dir_data, "metadata.json")
        JSONFile(file_path).write(self.__dict__)
        log.debug(f"Wrote {file_path}")
