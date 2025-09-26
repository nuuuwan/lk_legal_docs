from functools import cached_property

import urllib3
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from utils import Log

from utils_future.www.WWWSSLMixin import WWWSSLMixin

log = Log("WebPage")

urllib3.disable_warnings(InsecureRequestWarning)


class WWW(WWWSSLMixin):
    TIMEOUT = 120

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        + "AppleWebKit/537.36 (KHTML, like Gecko) "
        + "Chrome/127.0.0.0 Safari/537.36"
    }

    def __init__(self, url):
        self.url = url

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, value):
        if not isinstance(value, WWW):
            return False
        return self.url == value.url

    def __str__(self):
        return f"🌐 {self.url}"

    @cached_property
    def content(self):
        try:
            response = WWW.get_session().get(
                self.url,
                verify=False,
                timeout=self.TIMEOUT,
                headers=self.HEADERS,
            )
            response.raise_for_status()
            content = response.text
            log.debug(f"Opened {self} ({len(content):,}B)")
            return content
        except Exception as e:
            log.error(f"[{self}] Failed to open: {e}")
            return None

    @cached_property
    def soup(self):
        if not self.content:
            return None
        return BeautifulSoup(self.content, "html.parser")

    def download_binary(self, local_path):
        try:
            response = WWW.get_session().get(
                self.url,
                timeout=self.TIMEOUT,
                verify=False,
                headers=self.HEADERS,
            )
            print(response.status_code)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(response.content)
            log.debug(f"Downloaded {self.url} to {local_path}")
        except Exception as e:
            log.error(f"Failed to download {self.url}: {e}")
            return
