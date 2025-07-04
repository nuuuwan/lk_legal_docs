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
