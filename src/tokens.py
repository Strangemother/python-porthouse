
from collections import defaultdict

from loguru import logger
dlog = logger.debug
elog = logger.error


USERS = {
    'user': {
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


TOKENS = {
    '1234': {
        # The user owning the socket.
        'owner': 'user',
        # Max sockets per token
        'max_connections': 5,
        'inherit_subscriptions': True,
        # 'subscriptions': {}
    },

    '1111': {
        'owner': 'user',
        'max_connections': 6,

        'inherit_subscriptions': False,
        'auto_subscribe': True,
        'subscriptions': {
            'beta': {
                'permissions': {'read'}
            }
        }
    },

}


class TokenCache:
    concurrent_count = 0
    sockets = set()


CACHE = defaultdict(TokenCache)


def exists(token):
    return TOKENS.get(token) is not None


def get_owner(token):
    token_obj = token
    if isinstance(token, str):
        token_obj = get_token_object(token)
    username = token_obj.get('owner')
    return USERS[username]


def get_token_object(token):
    return TOKENS[token]


def use_token(socket_id, token):
    item = CACHE[token]
    obj = get_token_object(token)

    ok = item.concurrent_count < obj['max_connections']

    item.concurrent_count += 1
    item.sockets.add(socket_id)
    dlog(f'use_token ({ok}), {socket_id}, {token}: {item.sockets}')

    return ok


def unuse_token(socket_id, token=None):
    dlog(f'unuse_token, {socket_id}, {token}')
    item = CACHE.get(token)
    if item is not None:
        item.concurrent_count -= 1
        item.sockets.remove(socket_id)
    else:
        elog('Cannot unuse unknown socket_id token')