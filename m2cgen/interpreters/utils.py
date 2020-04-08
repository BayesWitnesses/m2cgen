from collections import namedtuple


CacheResult = namedtuple('CacheResult', ['var_name', 'expr_result'])


def get_file_content(path):
    with open(path) as f:
        return f.read()
