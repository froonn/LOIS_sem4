"""
Выполнил студент группы 321701:
- Мотолянец Кирилл Андреевич
Вариант 6

Парсер формул сокращенного языка логики высказываний
23.05.2025

Источники:
- Логические основы интеллектуальных систем. Практикум : учебно - метод. пособие / В. В. Голенков [и др.]. – Минск : БГУИР, 2011. – 70 с. : ил.
"""

from typing import Optional, List, Tuple

from logical_interpreter.logical_interpreter.log_ast import *
from logical_interpreter.logical_interpreter.log_lexer import log_lex


class LogicalFormula:
    """
    Class representing a logical formula.

    Attributes:
        ast (Expr): The abstract syntax tree of the logical formula.
        vars (set[str]): The set of variables in the logical formula.
    """

    def __init__(self, ast: Expr, variables: list[str]) -> None:
        """
        Initializes a LogicalFormula instance.

        Args:
            ast (Expr): The abstract syntax tree of the logical formula.
            variables (set[str]): The list of variables in the logical formula.
        """
        self.ast = ast
        self.vars = variables

    def __call__(self, kwargs: dict[str, bool]) -> bool:
        """
        Evaluates the logical formula with the given variable assignments.

        Args:
            kwargs (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of evaluating the logical formula.
        """
        return self.ast.eval(kwargs)

    def __eq__(self, other: object) -> bool:
        """
        Compares two LogicalFormula objects for equality.

        Args:
            other (object): Another object to compare.

        Returns:
            bool: True if the formulas are equivalent, False otherwise.
        """
        if not isinstance(other, LogicalFormula):
            return NotImplemented

        if self.vars != other.vars:
            return False

        from itertools import product
        for values in product([0, 1], repeat=len(self.vars)):
            env = dict(zip(self.vars, values))
            if self(env) != other(env):
                return False

        return True


class Parser:
    """
    A parser for logical formulas.

    Attributes:
        tokens (list[tuple[str, str]]): The list of tokens to parse.
        pos (int): The current position (index) in the token list.
    """

    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        """
        Initializes the Parser instance.

        Args:
            tokens (list[tuple[str, str]]): The list of tokens to parse.
        """
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Expr:
        """
        Parses the entire token list into an abstract syntax tree (AST).
        Ensures that all tokens are consumed after a successful parse.

        Returns:
            Expr: The root of the parsed AST.

        Raises:
            SyntaxError: If the formula is syntactically incorrect, or if unconsumed tokens remain.
        """
        result = self.expression()
        if self.pos < len(self.tokens):
            raise SyntaxError(f'Unexpected token at the end of the formula: {self.tokens[self.pos][0]}')
        return result

    def match(self, expected_tag: str) -> Optional[str]:
        """
        Attempts to match the current token's tag with the `expected_tag`.
        If a match is found, the parser's position is advanced (`self.pos` is incremented).

        Args:
            expected_tag (str): The tag of the token expected (e.g., 'LPAREN', 'VAR').

        Returns:
            Optional[str]: The matched token's lexeme (value, e.g., '(' or 'A'),
                           or `None` if no match is found.
        """
        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == expected_tag:
            self.pos += 1
            return self.tokens[self.pos - 1][0]
        return None

    def peek_binary_op(self) -> Optional[str]:
        """
        Peeks at the current token to check if it is a binary operator
        without advancing the parser's position.

        Returns:
            Optional[str]: The tag of the binary operator ('AND', 'OR', 'IMPLIES', 'EQUIV'),
                           or `None` if the current token is not a binary operator.
        """
        if self.pos < len(self.tokens):
            tag = self.tokens[self.pos][1]
            if tag in ('AND', 'OR', 'IMPLIES', 'EQUIV'):
                return tag
        return None

    def atom(self) -> Optional[Expr]:
        """
        Attempts to parse an atomic expression (variable or constant).
        This method is non-consuming if no atom is found, allowing other parsing
        paths to be attempted.

        Returns:
            Optional[Expr]: An `Expr` node representing the parsed atom (e.g., `Var`, `ConstTrue`),
                            or `None` if the current token is not an atomic expression.
        """
        var_lexeme = self.match('VAR')
        if var_lexeme:
            return Var(var_lexeme)

        if self.match('TRUE'):
            return ConstTrue()

        if self.match('FALSE'):
            return ConstFalse()

        return None

    def expression(self) -> Expr:
        """
        Parses a logical expression.

        Returns:
            Expr: The parsed expression node in the AST.

        Raises:
            SyntaxError: If the expression does not conform to the strict rules,
                         e.g., missing parentheses, unexpected tokens, or
                         operations without strict encapsulation.
        """
        atom_node = self.atom()
        if atom_node:
            return atom_node

        if not self.match('LPAREN'):
            raise SyntaxError('Expected an atomic expression (variable/constant) or '
                              'an opening parenthesis for an operation (e.g., (A&B) or (!A)).')

        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == 'NOT':
            self.pos += 1
            operand = self.expression()
            if not self.match('RPAREN'):
                raise SyntaxError('Expected closing parenthesis `)` after NOT operation (e.g., (!A)).')
            return Not(operand)
        else:
            inner_expr = self.expression()

            op_tag = self.peek_binary_op()

            if op_tag:
                self.pos += 1
                right_operand = self.expression()

                if not self.match('RPAREN'):
                    raise SyntaxError('Expected closing parenthesis `)` after binary operation (e.g., (A&B)).')

                if op_tag == 'AND':
                    return And(inner_expr, right_operand)
                elif op_tag == 'OR':
                    return Or(inner_expr, right_operand)
                elif op_tag == 'IMPLIES':
                    return Implies(inner_expr, right_operand)
                elif op_tag == 'EQUIV':
                    return Equiv(inner_expr, right_operand)
                else:
                    raise SyntaxError(f"Internal parser error: Unrecognized binary operator tag: {op_tag}")
            else:
                if not self.match('RPAREN'):
                    raise SyntaxError('Expected a binary operator or closing parenthesis after '
                                      'the expression inside parentheses. If the expression is atomic and standalone (e.g., A), '
                                      'it does not require outer parentheses, but if enclosed, '
                                      'it must be in the format `(Expression)` or part of `(Expression Operator Expression)`.')
                return inner_expr


def parse(logical_formula: str) -> LogicalFormula:
    """
    Parses a logical formula string into a LogicalFormula object.

    Args:
        logical_formula (str): The logical formula as a string.

    Returns:
        LogicalFormula: The parsed logical formula.
    """
    tokens = log_lex(logical_formula)
    parser = Parser(tokens)
    ast = parser.parse()

    variables = set()
    for token in tokens:
        if token[1] == 'VAR':
            variables.add(token[0])

    return LogicalFormula(ast, variables)
