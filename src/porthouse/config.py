LOG_LEVEL = 'debug'


HOST = '127.0.0.1'
DEBUG = True
RELOAD = DEBUG
PORT = 0# 9004

BALANCE_PORTS = (9004, 9005,)
BALANCE_ADDRESSES = (HOST, BALANCE_PORTS, )

INGRESS_APP = 'porthouse.ingress:app'

ROUTING = 'supercast'

mb1 = 1024 * 1024
mb16 = 16 * mb1

WS_MAX_SIZE = mb1

