import ssl

import aiohttp

from .auth import AioZjAuth


class AioZj(AioZjAuth):

    def __init__(self, app_id, app_secret, timeout=5):
        """
        :param app_id: appid
        :param app_secret:  secret
        :param timeout: 连接字节网关超时事件，单位秒
        """
        conn = aiohttp.TCPConnector(limit=1024)
        self._session = aiohttp.ClientSession(
            connector=conn, skip_auto_headers={'Content-Type'},
        )
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
