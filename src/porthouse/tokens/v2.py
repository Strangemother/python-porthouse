
from collections import defaultdict

from loguru import logger
dlog = logger.debug
elog = logger.error


USERS = {
    'admin': {
        'username': 'admin',
        # A user can create non persistent rooms.
        'can_create_transient': True,
        # max over all concurrent sockets
        'max_connections': 100,
        # max amount of allowed unique tokens.
        'max_tokens': 100,
        # how many connections a single token
        # may create concurrently.
        'max_connections_per_token': 50,
        'max_peristent_rooms': 20,
        'max_transient_rooms': 10,
        'subscriptions': {
            'alpha': {
            },

            'beta': {
            }
        }
    }
}


class TokenStruct:
    populated = False
    id = None
    # owner = 'user'
    # max_connections = 6
    # inherit_subscriptions = False
    # auto_subscribe = True
    # subscriptions = {
    #         'beta': {
    #             'permissions': {'read'}
    #         }
    #     }
    UNDEFINED = {}

    def set_data(self, content):
        self.__dict__.update(content)

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=UNDEFINED):
        res = getattr(self, key, default)
        if res is self.UNDEFINED:
            raise KeyError(f"Missing {key=}")
        return res


class TokenCache:
    concurrent_count = 0
    sockets = set()


# CACHE = defaultdict(TokenCache)
# TOKENS = defaultdict(TokenStruct)

import httpx

ASK_URL = 'http://localhost:8000/tokens/ask/'
# PRESENT_URL = 'http://localhost:8000/tokens/present/'
EXISTS_URL = 'http://localhost:8000/tokens/exists/'
DETAIL_URL = 'http://localhost:8000/tokens/info/'

#  data = {'message': 'Hello, world!'}
# >>> files = {'file': open('report.xls', 'rb')}
# >>> r = httpx.post("https://httpbin.org/post", data=data, files=files)

## A random first string. This will be removed later
tokenizer_onboarding_token = 35289759287529875

# post_token = None

class RequestFlow(object):

    post_token = None

    ASK_URL_FORMAT = '{host}/tokens/ask/'
    # PRESENT_URL_FORMAT = '{host}/tokens/present/'
    EXISTS_URL_FORMAT = '{host}/tokens/exists/'
    DETAIL_URL_FORMAT = '{host}/tokens/info/'

    async def ask(self, onboarding_token, url=None):
        can_tokenize = True
        # global post_token
        async with httpx.AsyncClient() as client:
            data = {'token': onboarding_token }
            aurl = self.ASK_URL_FORMAT.format(host=self.api_endpoint)
            r = await client.post(url or aurl, data=data)
            can_tokenize = r.is_success
            if can_tokenize:
                self.post_token = r.json()
        return can_tokenize

    async def fetch_info(self, token, url=None):
        async with httpx.AsyncClient() as client:
            data = {'token': token }
            data.update(self.post_token)

            url = url or self.DETAIL_URL_FORMAT.format(host=self.api_endpoint)
            r = await client.post(url, data=data)
            if r.is_success:
                d = r.json()
                dlog(f'fetch_info: {d}')
                return d
            else:
                elog(f'Error {r}')

        elog(f'No return from fetch_info({token=})')
        return {}

    async def exists(self, token, url=None):
        async with httpx.AsyncClient() as client:
            data = {'token': token }
            data.update(self.post_token)
            url = url or self.EXISTS_URL_FORMAT.format(host=self.api_endpoint)
            r = await client.post(url, data=data)
            if r.is_success:
                d = r.json()
                print('Token exists result:', d)
                ok = d['exists']
                if ok:
                    return ok
                print('Token', token, 'was not accepted by the host', url)

        return self.TOKENS.get(token) is not None


class Tokens(RequestFlow):

    CACHE = None

    def __init__(self, api_endpoint='', tokenizer_onboarding_token=None):
        self.CACHE = defaultdict(TokenCache)
        self.TOKENS = defaultdict(TokenStruct)
        self.api_endpoint = api_endpoint
        self.onboarding_token = tokenizer_onboarding_token

    async def use_token(self, socket_id, token):
        item = self.CACHE[token]
        obj = await self.get_token_object(token)

        ok = item.concurrent_count < obj['max_connections']

        item.concurrent_count += 1
        item.sockets.add(socket_id)
        dlog(f'use_token ({ok}), {socket_id}, {token}: {item.sockets}')
        return ok

    async def unuse_token(self, socket_id, token=None):
        dlog(f'unuse_token, {socket_id}, {token}')
        item = self.CACHE.get(token)
        if item is not None:
            item.concurrent_count -= 1
            item.sockets.remove(socket_id)
        else:
            elog('Cannot unuse unknown socket_id token')

    async def get_token_object(self, token):
        dlog(f'looking for token info on {token=}')
        val = self.TOKENS[token]

        if val.populated is False:
            val.id = token
            res = await self.fetch_info(token)
            val.set_data(res)
            val.populated = True
        else:
            dlog('Using cached object', val)
        return val

    async def get_owner(self, token):
        token_obj = token
        if isinstance(token, str):
            token_obj = await self.get_token_object(token)
        username = token_obj.get('owner')
        try:
            return USERS[username]
        except KeyError as err:
            elog(f'{username=} is not in USERS')
            raise err


