import uuid
import re


class Envelope(object):
    """A Class to wrap the message through
    the coms layer. The client doesn't usually see
    the envelope.
    """
    def __init__(self, content, owner):
        self.content = content
        self._uuid = str(uuid.uuid4())

    @classmethod
    def wrap(cls, str_content, owner, type='websocket.receive'):
        obj = {
            'type': type,
            'text': str_content,
        }
        return cls(obj, owner)

    @property
    def id(self):
        return self._uuid

    @property
    def destination(self):
        # return self.content['text'].split()[0]
        text = self.content.get('text') or self.content
        if isinstance(text, str):
            return parse_destination(text)

        if isinstance(text, dict):
            return text.get('destination', None)


def parse_destination(text, key='destination'):
    """Collect the assignments within the text for the
    given key:

        parse_destination(text, key='destination')

    Will capture ['A','V', 'S'] for these formats:

        destination: A V S
        destination:A V S
        destination:      A V S
        destination     A V S
        destination::       A V S

    """
    pattern = r'%s[:]{0,}[ ]{0,}(.+?)\n' % key
    match = re.search(pattern, text)
    if match:
        destinations = match.group(1).split()
        return destinations
    return []

# Test the function
# print(parse_destination('destination A B C\n'))
