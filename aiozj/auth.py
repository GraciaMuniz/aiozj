import asyncio
import json

from .exception import (
    AioZjTimeoutError,
    AioZjAuthError,
)


class AioZjAuth:

    async def _do_auth_get(self, url):
        try:
            async with self._session.get(url, timeout=self.timeout) as resp:
                if resp.status != 200:
                    raise AioZjAuthError()
                body = await resp.text(encoding='utf-8')
                json_body = json.loads(body)
                errcode = json_body.get('errcode')
                if errcode and errcode != 0:
                    raise AioZjAuthError(json.dumps(json_body))
                return json_body
        except asyncio.TimeoutError:
            raise AioZjTimeoutError()

    async def get_access_token(self):
        url = 'https://developer.toutiao.com/api/apps/token' \
              '?grant_type=client_credential&appid={}&secret={}'.format(
            self.app_id, self.app_secret)
        json_body = await self._do_auth_get(url)
        return json_body.get('access_token')

    class Code2SessionResult:

        def __init__(self, open_id, session_key, anonymous_openid=None):
            self.open_id = open_id
            self.session_key = session_key
            self.anonymous_openid = anonymous_openid

    async def code2session(self, code=None, anonymous_code=None):
        if not code and not anonymous_code:
            raise AioZjAuthError('Either code or anonymous_code is required')
        params = {
            'appid': self.app_id,
            'secret': self.app_secret,
        }
        if code:
            params['code'] = code
        if anonymous_code:
            params['anonymous_code'] = anonymous_code

        access_token_url = \
            'https://developer.toutiao.com/api/apps/jscode2session'.format(
                **params)

        try:
            async with self._session.get(access_token_url, params=params,
                                         timeout=self.timeout) as resp:
                if resp.status != 200:
                    raise AioZjAuthError()
                body = await resp.text()
                json_body = json.loads(body)
                errcode = json_body.get('errcode')
                if errcode and errcode != 0:
                    raise AioZjAuthError(json.dumps(json_body))

                open_id = json_body.get('openid')
                session_key = json_body.get('session_key')
                anonymous_openid = json_body.get('anonymous_openid')
                return self.Code2SessionResult(open_id, session_key,
                                               anonymous_openid)

        except asyncio.TimeoutError:
            raise AioZjTimeoutError()
