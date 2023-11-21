
from collections import defaultdict

from loguru import logger
dlog = logger.debug
elog = logger.error


USERS = {
    'admin': {
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


# TOKENS = {
#     '1234': {
#         # The user owning the socket.
#         'owner': 'user',
#         # Max sockets per token
#         'max_connections': 5,
#         'inherit_subscriptions': True,
#         # 'subscriptions': {}
#     },

#     '1111': {
#         'owner': 'user',
#         'max_connections': 6,

#         'inherit_subscriptions': False,
#         'auto_subscribe': True,
#         'subscriptions': {
#             'beta': {
#                 'permissions': {'read'}
#             }
#         }
#     },

# }


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


CACHE = defaultdict(TokenCache)
TOKENS = defaultdict(TokenStruct)

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

post_token = None

async def ask(onboarding_token, url=None):
    can_tokenize = True
    global post_token
    async with httpx.AsyncClient() as client:
        data = {'token': onboarding_token }
        r = await client.post(url or ASK_URL, data=data)
        can_tokenize = r.is_success
        if can_tokenize:
            post_token = r.json()
    return can_tokenize


async def exists(token, url=None):
    async with httpx.AsyncClient() as client:
        data = {'token': token }
        data.update(post_token)
        url = url or EXISTS_URL
        r = await client.post(url, data=data)
        if r.is_success:
            d = r.json()
            print('Token exists result:', d)
            ok = d['exists']
            if ok:
                return ok
            print('Token', token, 'was not accepted by the host', url)

    return TOKENS.get(token) is not None


async def fetch_info(token, url=None):
    async with httpx.AsyncClient() as client:
        data = {'token': token }
        data.update(post_token)

        url = url or DETAIL_URL
        r = await client.post(url, data=data)
        if r.is_success:
            d = r.json()
            dlog(f'fetch_info: {d}')
            return d
        else:
            elog(f'Error {r}')

    elog(f'No return from fetch_info({token=})')
    return {}


async def get_owner(token):
    token_obj = token
    if isinstance(token, str):
        token_obj = await get_token_object(token)
    username = token_obj.get('owner')
    try:
        return USERS[username]
    except KeyError as err:
        elog(f'{username=} is not in USERS')
        raise err


async def get_token_object(token):
    dlog(f'looking for token info on {token=}')
    val = TOKENS[token]

    if val.populated is False:
        val.id = token
        res = await fetch_info(token)
        val.set_data(res)
        val.populated = True
    else:
        dlog('Using cached object', val)
    return val


async def use_token(socket_id, token):
    item = CACHE[token]
    obj = await get_token_object(token)

    ok = item.concurrent_count < obj['max_connections']

    item.concurrent_count += 1
    item.sockets.add(socket_id)
    dlog(f'use_token ({ok}), {socket_id}, {token}: {item.sockets}')

    return ok


async def unuse_token(socket_id, token=None):
    dlog(f'unuse_token, {socket_id}, {token}')
    item = CACHE.get(token)
    if item is not None:
        item.concurrent_count -= 1
        item.sockets.remove(socket_id)
    else:
        elog('Cannot unuse unknown socket_id token')