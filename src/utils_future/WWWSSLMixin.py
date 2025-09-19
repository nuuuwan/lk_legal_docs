import ssl

import requests
from requests.adapters import HTTPAdapter


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
