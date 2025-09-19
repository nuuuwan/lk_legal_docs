import ssl
from functools import cached_property

import requests
import urllib3
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.exceptions import InsecureRequestWarning
from utils import Log

log = Log("WebPage")

urllib3.disable_warnings(InsecureRequestWarning)


class WWWSSLMixin:
    class SSLAdapter(HTTPAdapter):
        def __init__(self, ssl_context: ssl.SSLContext, **kwargs):
            self._ctx = ssl_context
            super().__init__(**kwargs)

        def init_poolmanager(
            self, connections, maxsize, block=False, **pool_kwargs
        ):
            pool_kwargs["ssl_context"] = self._ctx
            return super().init_poolmanager(
                connections, maxsize, block, **pool_kwargs
            )

        def proxy_manager_for(self, proxy, **proxy_kwargs):
            proxy_kwargs["ssl_context"] = self._ctx
            return super().proxy_manager_for(proxy, **proxy_kwargs)

    @staticmethod
    def get_session() -> requests.Session:
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT:@SECLEVEL=1")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        s = requests.Session()
        s.mount("https://", WWWSSLMixin.SSLAdapter(ctx))
        return s


class WWW(WWWSSLMixin):
    TIMEOUT = 120

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
                self.url, timeout=self.TIMEOUT, verify=False
            )
            response.raise_for_status()
            content = response.text
            log.debug(f"[{self}] Opened. {len(content):,}B")
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
                self.url, timeout=self.TIMEOUT, verify=False
            )
            print(response.status_code)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(response.content)
            log.info(f"Downloaded {self.url} to {local_path}")
        except Exception as e:
            log.error(f"Failed to download {self.url}: {e}")
            return
