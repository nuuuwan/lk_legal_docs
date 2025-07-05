import os
import time
from functools import cached_property

import requests
from bs4 import BeautifulSoup
from utils import Log

log = Log("WebPage")


class WebPage:
    BASE_URL = "https://documents.gov.lk"
    T_SLEEP = 5
    T_TIMEOUT = 60

    def __init__(self, url):
        assert url.startswith(self.BASE_URL)
        self.url = url

    @cached_property
    def content(self):
        response = requests.get(self.url)
        log.debug(f"🌐 [{response.status_code}] {self.url}")
        response.raise_for_status()
        return response.text

    @cached_property
    def soup(self):
        return BeautifulSoup(self.content, "html.parser")

    @staticmethod
    def sleep():
        time.sleep(WebPage.T_SLEEP)

    def download_binary(self, file_path):
        response = requests.get(
            self.url, stream=True, timeout=WebPage.T_TIMEOUT
        )
        log.debug(f"🌐 [{response.status_code}] {self.url}")
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        file_size_k = os.path.getsize(file_path) / (1_000)
        log.debug(f"Wrote {file_path} ({file_size_k:.1f} KB)")
