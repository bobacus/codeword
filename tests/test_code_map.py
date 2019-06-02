import unittest

from codeword.code_map import CodeMap

class TestCodeMap(unittest.TestCase):
    def test_repr_0(self):
        code_map = CodeMap({})

        self.assertEqual(repr(code_map), 'CodeMap({})')

    def test_repr_1(self):
        code_map = CodeMap({1: 'A'})

        self.assertEqual(repr(code_map), 'CodeMap({1: \'A\'})')

    def test_repr_2x(self):
        code_map = CodeMap({1: 'A', 13: 'Z'})

        self.assertEqual(repr(code_map), 'CodeMap({1: \'A\', 13: \'Z\'})')

    def test_eq_0_0(self):
        a = CodeMap({})
        b = CodeMap({})

        self.assertEqual(a, b)

    def test_eq_0_1(self):
        a = CodeMap({})
        b = CodeMap({1: 'A'})

        self.assertNotEqual(a, b)

    def test_str_0(self):
        code_map = CodeMap({})

        self.assertEqual(str(code_map), '.' * 26)

    def test_str_1(self):
        code_map = CodeMap({1: 'A'})

        self.assertEqual(str(code_map), 'A' + ('.' * 25))

    def test_str_9(self):
        code_map = CodeMap({9: 'A'})

        self.assertEqual(str(code_map), '........A' + ('.' * 17))
