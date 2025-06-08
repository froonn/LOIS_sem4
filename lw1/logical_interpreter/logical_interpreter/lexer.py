"""
Выполнил студент группы 321701:
- Мотолянец Кирилл Андреевич
Вариант 6

Лексический анализатор, который токенизирует строку на основе полученного шаблона токенов.
23.05.2025

Источники:
- Логические основы интеллектуальных систем. Практикум : учебно - метод. пособие / В. В. Голенков [и др.]. – Минск : БГУИР, 2011. – 70 с. : ил.
"""

from typing import List, Tuple, Optional


def lex(characters: str, token_patterns: List[Tuple[str, Optional[str]]]) -> List[Tuple[str, str]]:
    """
    Lexical analyzer that splits a string into tokens using specified patterns.

    Args:
        characters (str): The input string to tokenize.
        token_patterns: List of patterns and tags (pattern, tag/None).

    Returns:
        List[Tuple[str, str]]: List of tokens (text, tag).

    Raises:
        SyntaxError: If an unknown character is encountered.
    """

    pos = 0
    tokens = []
    length = len(characters)

    while pos < length:
        match_found = False

        if characters[pos].isspace():
            pos += 1
            continue

        for pat, tag in token_patterns:
            if pat is None:
                continue

            if pat == '[VAR]':
                if characters[pos].isalpha():
                    start = pos
                    pos += 1
                    while pos < length and characters[pos].isalnum():
                        pos += 1
                    tokens.append((characters[start:pos], tag))
                    match_found = True
                    break
            elif pat == '[WS]':
                pass
            else:
                pat_len = len(pat)
                if characters.startswith(pat, pos):
                    if tag is not None:
                        tokens.append((pat, tag))
                    pos += pat_len
                    match_found = True
                    break

        if not match_found:
            raise SyntaxError(f'Illegal character: {characters[pos]!r}\n')

    return tokens
