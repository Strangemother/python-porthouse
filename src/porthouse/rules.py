
"""
Check the token. If the token is owned by the correct client
accept, else ditch and msg the client.
"""

from loguru import logger
dlog = logger.debug

from . import tokens

class Rule(object):

    check_port = True

    def __init__(self, **extras):
        self.__dict__.update(**extras)

    async def is_valid(self, websocket):
        pass


class IPAddressRule(Rule):
    host = None

    async def is_valid(self, websocket, **extras):
        if self.check_port is True:
            return websocket.headers['host'] == self.host
        return websocket.client.host == self.host


class TokenRule(Rule):
    param = None

    async def is_valid(self, websocket, **extras):
        token = extras.get(self.param, None)
        exists = await self.tokens.exists(token)
        return exists


class RuleSet(object):

    def __init__(self, *rules):
        self.rules = rules

    async def is_valid(self, websocket, **extras):
        for rule in self.rules:
            if await rule.is_valid(websocket, **extras) is False:
                dlog(f'failed rule {rule}')
                return False
        return True
