import os
from dataclasses import dataclass
from functools import cached_property

from utils import File, JSONFile, Log

from lld.www.common.WebPage import WebPage

log = Log("Metadata")


@dataclass
class Metadata:
    doc_num: str
    date: str
    description: str
    source_url_en: str
    source_url_si: str
    source_url_ta: str

    @classmethod
    def get_doc_type_name(cls):
        raise NotImplementedError

    @cached_property
    def year(self):
        return self.doc_num.split("/")[1]

    @cached_property
    def year_doc_num(self):
        return self.doc_num.split("/")[0]

    @classmethod
    def get_doc_type_dir(cls):
        return os.path.join("data", cls.get_doc_type_name())

    @cached_property
    def dir_data(self):
        dir_data = os.path.join(self.get_doc_type_dir(), self.year, self.id)
        os.makedirs(dir_data, exist_ok=True)
        return dir_data

    @cached_property
    def id(self):
        return f"{self.year}-{self.year_doc_num}"

    def download_all(self):
        did_hot_download = False
        for lang, url in [
            ("en", self.source_url_en),
            ("si", self.source_url_si),
            ("ta", self.source_url_ta),
        ]:
            file_path = os.path.join(self.dir_data, f"{lang}.pdf")
            if not os.path.exists(file_path):
                page = WebPage(url)
                page.download_binary(file_path)
                did_hot_download = True

        return did_hot_download

    def write(self):
        file_path = os.path.join(self.dir_data, "metadata.json")
        JSONFile(file_path).write(self.__dict__)
        log.debug(f"Wrote {file_path}")

    @property
    def readme_lines(self):
        return [
            f"# [{self.doc_num}] {self.description}",
            "",
            f"**Date:** {self.date}",
            "",
            "## Original Sources",
            "",
            f"- [English]({self.source_url_en})",
            f"- [Sinhala]({self.source_url_si})",
            f"- [Tamil]({self.source_url_ta})",
        ]

    def write_readme(self):
        readme_path = os.path.join(self.dir_data, "README.md")
        File(readme_path).write_lines(self.readme_lines)
        log.debug(f"Wrote {readme_path}")

    @classmethod
    def get_metadata_file_path_lists(cls):
        file_path_lists = []
        for year in os.listdir(cls.get_doc_type_dir()):
            dir_data_for_year = os.path.join(cls.get_doc_type_dir(), year)
            for id in os.listdir(dir_data_for_year):
                dir_data = os.path.join(dir_data_for_year, id)
                file_path = os.path.join(dir_data, "metadata.json")
                if not os.path.exists(file_path):
                    log.warning(f"Metadata file not found: {file_path}")
                    continue
                file_path_lists.append(file_path)
        return file_path_lists

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
    def list_all(cls):
        metadata_file_path_lists = cls.get_metadata_file_path_lists()
        doc_metadata_list = [
            cls.from_file(file_path) for file_path in metadata_file_path_lists
        ]
        doc_metadata_list.sort(key=lambda x: x.id, reverse=True)
        log.info(f"Found {len(doc_metadata_list):,} docs.")
        return doc_metadata_list
