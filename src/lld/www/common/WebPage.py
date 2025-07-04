from functools import cached_property

import requests
from bs4 import BeautifulSoup
from utils import Log

log = Log('WebPage')


class WebPage:
    BASE_URL = "https://documents.gov.lk"

    def __init__(self, url):
        assert url.startswith(self.BASE_URL)
        self.url = url

    @cached_property
    def content(self):
        response = requests.get(self.url)
        log.debug(
            f'Fetching content from {
                self.url}, status code: {
                response.status_code}'
        )
        response.raise_for_status()
        return response.text

    @cached_property
    def soup(self):
        return BeautifulSoup(self.content, "html.parser")
