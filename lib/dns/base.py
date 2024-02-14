from typing import Callable

from requests import Session


class RequestHandler:
    _BASE_URL_FORMAT = "{scheme}://{host}/"

    def __init__(self,
                 scheme: str,
                 host: str,
                 auth: tuple,
                 verify: bool,
                 handler_maker: Callable = Session
                 ) -> None:

        self._handler = handler_maker()
        self._handler.auth = auth
        self._handler.verify = verify
        self._base_url = RequestHandler._BASE_URL_FORMAT.format(scheme=scheme, host=host)

    def get(self, url: str, **kwargs):
        url = self._base_url + url

        return self._handler.get(url, **kwargs)
