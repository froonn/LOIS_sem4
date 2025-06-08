"""
Выполнил студент группы 321701:
- Мотолянец Кирилл Андреевич
Вариант 6

Класс тестов для проверки корректности работы логического интерпретатора.
23.05.2025

Источники:
- Логические основы интеллектуальных систем. Практикум : учебно - метод. пособие / В. В. Голенков [и др.]. – Минск : БГУИР, 2011. – 70 с. : ил.
"""

import unittest
from logical_interpreter.logical_interpreter.log_parser import parse

class TestParser(unittest.TestCase):
    def test_equal(self):
        self.assertTrue(parse('1') == parse('1'))
        self.assertTrue(parse('(!1)') == parse('0'))
        self.assertTrue(parse('((!A)\\/B)') == parse('(A->B)'))
        self.assertTrue(parse('(A -> B)') == parse('((!B) -> (!A))'))

    def test_not_equal(self):
        self.assertFalse(parse('1') == parse('0'))
        self.assertFalse(parse('(!1)') == parse('1'))
        self.assertFalse(parse('((!A)\\/B)') == parse('(A/\\B)'))


    def test_syntax_error(self):
        with self.assertRaises(SyntaxError):
            parse('A /\\')
        with self.assertRaises(SyntaxError):
            parse('A \\/ B')
        with self.assertRaises(SyntaxError):
            parse('A /\\ (B \\/ C)')
        with self.assertRaises(SyntaxError):
            parse('(A \\/ B /\\ C)')
        with self.assertRaises(SyntaxError):
            parse('(!B \\/ C)')

if __name__ == '__main__':
    unittest.main()