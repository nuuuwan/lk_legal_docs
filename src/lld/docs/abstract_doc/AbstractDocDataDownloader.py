import os
import shutil
import tempfile
from functools import cached_property

from utils import Log

log = Log("AbstractDocDataDownloader")


class AbstractDocDataDownloader:
    DIR_TEMP = tempfile.gettempdir()
    DIR_TEMP_DATA = os.path.join(DIR_TEMP, "lk_legal_docs_data")

    @cached_property
    def dir_data(self):
        dir_data = os.path.join(self.get_doc_type_dir(), self.year, self.id)
        return dir_data

    @cached_property
    def dir_temp_data(self):
        return os.path.join(
            AbstractDocDataDownloader.DIR_TEMP_DATA, self.dir_data
        )

    def copy_metadata_to_temp_data(self):
        metadata_file_path = os.path.join(self.dir_data, "metadata.json")
        temp_metadata_file_path = os.path.join(
            self.dir_temp_data, "metadata.json"
        )
        if os.path.exists(temp_metadata_file_path):
            return False
        if not os.path.exists(self.dir_temp_data):
            os.makedirs(self.dir_temp_data, exist_ok=True)
        shutil.copyfile(metadata_file_path, temp_metadata_file_path)
        log.debug(f"Wrote {temp_metadata_file_path}")
        return True
