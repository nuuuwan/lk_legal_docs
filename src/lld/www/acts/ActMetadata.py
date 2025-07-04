import os
from dataclasses import dataclass
from functools import cached_property

from utils import JSONFile, Log

from lld.www.common import WebPage

log = Log('ActMetadata')


@dataclass
class ActMetadata:
    act_num: str
    date: str
    description: str
    source_url_en: str
    source_url_si: str
    source_url_ta: str

    @cached_property
    def year(self):
        return self.act_num.split('/')[1]

    @cached_property
    def year_act_num(self):
        return self.act_num.split('/')[0]

    @cached_property
    def dir_data(self):
        dir_data = os.path.join('data', 'acts', self.year)
        os.makedirs(dir_data, exist_ok=True)
        return dir_data

    @cached_property
    def file_prefix(self):
        return f"{self.year}-{self.year_act_num}"

    def download_all(self):
        did_hot_download = False
        for lang, url in [
            ("en", self.source_url_en),
            ("si", self.source_url_si),
            ("ta", self.source_url_ta),
        ]:
            file_path = os.path.join(
                self.dir_data, f"{self.file_prefix}-{lang}.pdf"
            )
            if not os.path.exists(file_path):
                page = WebPage(url)
                page.download_binary(file_path)
                did_hot_download = True

        return did_hot_download

    def write(self):
        file_path = os.path.join(
            self.dir_data, f"{self.file_prefix}-metadata.json"
        )
        JSONFile(file_path).write(self.__dict__)


    @staticmethod
    def get_metadata_file_path_lists():
        file_path_lists = []
        for year in os.listdir(os.path.join('data', 'acts')):
            dir_data = os.path.join('data', 'acts', year)
            for file_name in os.listdir(dir_data):
                file_path = os.path.join(dir_data, file_name)
                if file_name.endswith('-metadata.json'):
                    file_path_lists.append(file_path)
        return file_path_lists
    

    @classmethod
    def from_dict(cls, data):
        return cls(
            act_num=data['act_num'],
            date=data['date'],
            description=data['description'],
            source_url_en=data['source_url_en'],
            source_url_si=data['source_url_si'],
            source_url_ta=data['source_url_ta']
        )
    
    @classmethod
    def from_file(cls, file_path):
        data = JSONFile(file_path).read()
        return cls.from_dict(data)

    @staticmethod
    def list_all():
        metadata_file_path_lists = ActMetadata.get_metadata_file_path_lists()
        return [ActMetadata.from_file(file_path) for file_path in metadata_file_path_lists]
        