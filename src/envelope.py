import uuid


class Envelope(object):
    """A Class to wrap the message through
    the coms layer. The client doesn't usually see
    the envelope.
    """
    def __init__(self, content, owner):
        self.content = content
        self._uuid = str(uuid.uuid4())

    @property
    def id(self):
        return self._uuid

    @property
    def destination(self):
        return self.content['text'].split()[0]