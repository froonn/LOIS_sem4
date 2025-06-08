"""
Выполнил студент группы 321701:
- Мотолянец Кирилл Андреевич
Вариант 6

Лексический анализатор, который токенизирует строку на основе предопределенных шаблонов токенов.
23.05.2025

Источники:
- Логические основы интеллектуальных систем. Практикум : учебно - метод. пособие / В. В. Голенков [и др.]. – Минск : БГУИР, 2011. – 70 с. : ил.
"""

from typing import List, Tuple
from logical_interpreter.logical_interpreter import lexer

token_patterns = [
    ('->',     'IMPLIES'),
    ('/\\',    'AND'),
    ('\\/',    'OR'),
    ('!',      'NOT'),
    ('~',      'EQUIV'),
    ('(',      'LPAREN'),
    (')',      'RPAREN'),
    ('0',      'FALSE'),
    ('1',      'TRUE'),
    ('[VAR]',  'VAR'),
    ('[WS]',    None),
]


def log_lex(characters: str) -> List[Tuple[str, str]]:
    """
    Lexical analyzer that tokenizes a string based on predefined token patterns.

    Args:
        characters (str): The input string to be tokenized.

    Returns:
        list of tuples: A list of tokens where each token is a tuple containing the matched text and its corresponding tag.
    """
    return lexer.lex(characters, token_patterns)
