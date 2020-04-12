import re
from typing import List


def do_import(filename: str) -> List[str]:
    """Импортировать тектовый файл во внутренную структуру"""
    result = []
    with open(filename) as f:
        text = f.read()

    for line in re.split(r'\n+', text):
        ls = re.sub(r'([.,?])\s+', r'\1\n', line).split('\n')
        result.extend(ls)
        result.append('')
    return result
