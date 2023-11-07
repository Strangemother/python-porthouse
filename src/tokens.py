


TOKENS = {
    '1234': {
        # The user owning the socket.
        'owner': 'user',
        ## Max sockets per token
        'max_connections': 5,
    },
    'subscriptions': {
        'alpha': {
            'public': True
        },

        'beta': {
            'public': False
        }
    }
    # None: {
    #     'owner': 'system'
    # }
}


ROOMS = {
    'subscribers': {
        'user': {
            'permissions': {'read'}
        }
    }
}


def exists(token):
    return TOKENS.get(token) is not None
