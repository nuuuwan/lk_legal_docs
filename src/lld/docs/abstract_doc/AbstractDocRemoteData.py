from functools import cached_property


class AbstractDocRemoteData:
    @cached_property
    def remote_branch(self):
        return f"data_{self.decade}"

    @cached_property
    def remote_data_url(self):
        return (
            "https://github.com"
            + "/nuuuwan/lk_legal_docs_data"
            + f"/tree/{self.remote_branch}/data"
            + f"/{self.get_doc_type_name()}/{self.year}/{self.id}"
        )

    def get_remote_pdf_path(self, lang_code):
        return f"{self.remote_data_url}/{lang_code}.pdf"

    def get_remote_txt_path(self, lang_code):
        return f"{self.remote_data_url}/{lang_code}.txt"

    def get_remote_metadata_path(self):
        return f"{self.remote_data_url}/metadata.json"

    def download_all_data(self):
        is_hot = False
        is_hot |= self.copy_metadata_to_temp_data()
        is_hot |= self.download_pdfs()
        is_hot |= self.extract_text()
        return is_hot
