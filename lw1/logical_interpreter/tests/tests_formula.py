import unittest
from logical_interpreter.logical_interpreter.log_parser import parse

class TestParser(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(parse('1'), parse('1'))
        self.assertEqual(parse('(!1)'), parse('0'))
        self.assertEqual(parse('((!A)|B)'), parse('(A->B)'))

    def test_not_equal(self):
        self.assertNotEqual(parse('1'), parse('0'))
        self.assertNotEqual(parse('(!1)'), parse('1'))
        self.assertNotEqual(parse('((!A)|B)'), parse('(A&B)'))

if __name__ == '__main__':
    unittest.main()