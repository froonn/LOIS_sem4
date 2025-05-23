from typing import Optional, List, Tuple

from logical_interpreter.logical_interpreter.log_ast import *
from logical_interpreter.logical_interpreter.log_ast import Var, ConstTrue, ConstFalse
from logical_interpreter.logical_interpreter.log_lexer import log_lex


class LogicalFormula:
    """
    Class representing a logical formula.

    Attributes:
        ast (Expr): The abstract syntax tree of the logical formula.
        vars (list[str]): The list of variables in the logical formula.
    """

    def __init__(self, ast: Expr, variables: list[str]) -> None:
        """
        Initializes a LogicalFormula instance.

        Args:
            ast (Expr): The abstract syntax tree of the logical formula.
            variables (list[str]): The list of variables in the logical formula.
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

    variables = []
    for token in tokens:
        if token[1] == 'VAR' and token[0] not in variables:
            variables.append(token[0])

    return LogicalFormula(ast, variables)


class Parser:
    def __init__(self, tokens: List[Tuple[str, str]]) -> None:
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Expr:
        result = self.expression()
        if self.pos < len(self.tokens):
            raise SyntaxError(f'Unexpected token: {self.tokens[self.pos][0]}')
        return result

    def match(self, expected_tag: str) -> Optional[str]:
        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == expected_tag:
            self.pos += 1
            return self.tokens[self.pos - 1][0]
        return None

    def expression(self) -> Expr:
        return self.binary_operation(self.unary_operation_or_atom)

    def binary_operation(self, operand_parser) -> Expr:
        left = operand_parser()
        while True:
            op = self.peek_binary_op()
            if op:
                self.pos += 1
                right = operand_parser()
                if op == 'AND':
                    left = And(left, right)
                elif op == 'OR':
                    left = Or(left, right)
                elif op == 'IMPLIES':
                    left = Implies(left, right)
                elif op == 'EQUIV':
                    left = Equiv(left, right)
            else:
                break
        return left

    def unary_operation_or_atom(self) -> Expr:
        if self.match('LPAREN'):
            if self.match('NOT'):
                operand = self.expression()
                if not self.match('RPAREN'):
                    raise SyntaxError('Expected closing parenthesis after NOT operation')
                return Not(operand)
            else:
                self.pos -= 1  # Backtrack, it might be a parenthesized atom
                return self.atom_or_parenthesized_expression()
        else:
            return self.atom()

    def atom_or_parenthesized_expression(self) -> Expr:
        if self.match('LPAREN'):
            expr = self.expression()
            if not self.match('RPAREN'):
                raise SyntaxError('Expected closing parenthesis')
            return expr
        else:
            return self.atom()

    def atom(self) -> Expr:
        var = self.match('VAR')
        if var:
            return Var(var)
        if self.match('TRUE'):
            return ConstTrue()
        if self.match('FALSE'):
            return ConstFalse()
        raise SyntaxError('Expected variable or constant')

    def peek_binary_op(self) -> Optional[str]:
        if self.pos < len(self.tokens):
            tag = self.tokens[self.pos][1]
            if tag in ('AND', 'OR', 'IMPLIES', 'EQUIV'):
                return tag
        return None