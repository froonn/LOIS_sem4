"""
Выполнил студент группы 321701:
- Мотолянец Кирилл Андреевич
Вариант 6

Класс тестов для проверки корректности работы парсера.
23.05.2025

Источники:
- Логические основы интеллектуальных систем. Практикум : учебно - метод. пособие / В. В. Голенков [и др.]. – Минск : БГУИР, 2011. – 70 с. : ил.
"""


import unittest
from logical_interpreter.logical_interpreter.log_parser import parse, Parser
from logical_interpreter.logical_interpreter.log_ast import And, Or


class TestLogicalFormula(unittest.TestCase):
    def test_evaluates_simple_formula(self):
        formula = parse("(a /\\ b)")
        self.assertTrue(formula({'a': True, 'b': True}))
        self.assertFalse(formula({'a': True, 'b': False}))

    def test_evaluates_complex_formula(self):
        formula = parse("((a \\/ b) /\\ (!c))")
        self.assertTrue(formula({'a': True, 'b': False, 'c': False}))
        self.assertFalse(formula({'a': False, 'b': False, 'c': False}))

    def test_evaluates_equivalence(self):
        formula = parse("(a ~ b)")
        self.assertTrue(formula({'a': True, 'b': True}))
        self.assertFalse(formula({'a': True, 'b': False}))

    def test_evaluates_implication(self):
        formula = parse("(a -> b)")
        self.assertTrue(formula({'a': False, 'b': False}))
        self.assertFalse(formula({'a': True, 'b': False}))

    def test_handles_empty_formula(self):
        with self.assertRaises(SyntaxError):
            parse("")

    def test_handles_invalid_syntax(self):
        with self.assertRaises(SyntaxError):
            parse("a /\\ (b \\/")

class TestParser(unittest.TestCase):
    def test_parses_simple_expression(self):
        parser = Parser([('(', 'LPAREN'), ('a', 'VAR'), ('/\\', 'AND'), ('b', 'VAR'), (')', 'RPAREN')])
        ast = parser.parse()
        self.assertIsInstance(ast, And)

    def test_parses_nested_expression(self):
        parser = Parser([('(', 'LPAREN'), ('(', 'LPAREN'), ('a', 'VAR'), ('\\/', 'OR'), ('b', 'VAR'), (')', 'RPAREN'), ('/\\', 'AND'), ('c', 'VAR'), (')', 'RPAREN')])
        ast = parser.parse()
        self.assertIsInstance(ast, And)
        self.assertIsInstance(ast.left, Or)

    def test_handles_unexpected_token(self):
        parser = Parser([('a', 'VAR'), ('/\\', 'AND'), ('/\\', 'AND')])
        with self.assertRaises(SyntaxError):
            parser.parse()

    def test_handles_missing_closing_parenthesis(self):
        parser = Parser([('(', 'LPAREN'), ('a', 'VAR'), ('/\\', 'AND'), ('b', 'VAR')])
        with self.assertRaises(SyntaxError):
            parser.parse()

if __name__ == '__main__':
    unittest.main()