"""Helper functions for working with templates"""

import os
import re
from string import Template


class MyTemplate(Template):
    delimiter = '>>'


def render_template_file(path, **kwargs):
    with open(path, 'rb') as fp:
        raw = fp.read().decode('utf-8')

    content = MyTemplate(raw).substitute(**kwargs)

    render_path = path[:-len('.template')] if path.endswith('.template') else path
    with open(render_path, 'wb') as fp:
        fp.write(content.encode('utf-8'))
    if path.endswith('.template'):
        os.remove(path)


CAMELCASE_INVALID_CHARS = re.compile(r'[^a-zA-Z\d]')


def string_camelcase(string):
    """ Convert a word  to its CamelCase version and remove invalid chars

    >>> string_camelcase('miss-you')
    'MissYou'

    >>> string_camelcase('miss_you')
    'MissYou'

    """
    return CAMELCASE_INVALID_CHARS.sub('', string.title())
