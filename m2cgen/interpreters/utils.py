import re

from collections import namedtuple
from functools import lru_cache
from math import ceil, log

from m2cgen.ast import TOTAL_NUMBER_OF_EXPRESSIONS


CachedResult = namedtuple('CachedResult', ['var_name', 'expr_result'])


def get_file_content(path):
    with open(path) as f:
        return f.read()


@lru_cache(maxsize=1 << ceil(log(TOTAL_NUMBER_OF_EXPRESSIONS, 2)))
def _get_handler_name(expr_tpe):
    expr_name = _normalize_expr_name(expr_tpe.__name__)
    return "interpret_" + expr_name


def _normalize_expr_name(name):
    return re.sub("(?!^)([A-Z]+)", r"_\1", name).lower()
