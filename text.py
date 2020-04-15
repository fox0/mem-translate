"""
Слой логики по работе с текстом
"""
import re
from typing import List

PREFIX_TRANSLATE = '>>> '
PREFIX_CUT = '>>><<<'


def do_import(filename: str) -> List[str]:
    """Импортировать тектовый файл во внутренную структуру"""
    result = []
    with open(filename) as f:
        text = f.read()

    for line in re.split(r'\n+', text):
        line = re.sub(r'([.,?])\s+', r'\1\n', line)
        for seq in line.split('\n'):
            result.append(seq)
            result.append(PREFIX_TRANSLATE)
        result.append(PREFIX_CUT)
    return result
