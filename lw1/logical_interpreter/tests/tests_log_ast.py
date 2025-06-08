"""
Выполнил студент группы 321701:
- Мотолянец Кирилл Андреевич
Вариант 6

Класс тестов для проверки корректности работы абстрактного синтаксического дерева (AST) логических формул.
23.05.2025

Источники:
- Логические основы интеллектуальных систем. Практикум : учебно - метод. пособие / В. В. Голенков [и др.]. – Минск : БГУИР, 2011. – 70 с. : ил.
"""


import unittest

from logical_interpreter.logical_interpreter.log_ast import *

class TestLogicalOperations(unittest.TestCase):
    def test_variable_evaluation(self):
        env = {'a': True, 'b': False}
        self.assertTrue(Var('a').eval(env))
        self.assertFalse(Var('b').eval(env))

    def test_and_operation(self):
        env = {'a': True, 'b': False}
        self.assertFalse(And(Var('a'), Var('b')).eval(env))
        self.assertTrue(And(Var('a'), Var('a')).eval(env))

    def test_or_operation(self):
        env = {'a': True, 'b': False}
        self.assertTrue(Or(Var('a'), Var('b')).eval(env))
        self.assertFalse(Or(Var('b'), Var('b')).eval(env))

    def test_not_operation(self):
        env = {'a': True, 'b': False}
        self.assertFalse(Not(Var('a')).eval(env))
        self.assertTrue(Not(Var('b')).eval(env))

    def test_implies_operation(self):
        env = {'a': True, 'b': False}
        self.assertFalse(Implies(Var('a'), Var('b')).eval(env))
        self.assertTrue(Implies(Var('b'), Var('a')).eval(env))
        self.assertTrue(Implies(Var('b'), Var('b')).eval(env))

    def test_equiv_operation(self):
        env = {'a': True, 'b': False}
        self.assertFalse(Equiv(Var('a'), Var('b')).eval(env))
        self.assertTrue(Equiv(Var('a'), Var('a')).eval(env))
        self.assertTrue(Equiv(Var('b'), Var('b')).eval(env))

if __name__ == '__main__':
    unittest.main()