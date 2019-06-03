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

    def test_infer_new_key_from_word(self):
        code_map = CodeMap({9: 'A'})
        sequence = ('A', 3, 4)
        word = 'ARE'

        result = code_map.infer_new_key_from_word(sequence, word)

        self.assertEqual(result, CodeMap({3: 'R', 4: 'E', 9: 'A'}))

    def test_infer_new_key_from_word_inconsistent(self):
        code_map = CodeMap({9: 'A'})
        sequence = ('A', 3, 4)
        word = 'ASS'

        with self.assertRaises(ValueError):
            code_map.infer_new_key_from_word(sequence, word)

    def test_infer_new_key_from_word_4(self):
        code_map = CodeMap({2: 'O', 3: 'R', 4: 'E'})
        sequence = (1, 'R', 'E', 1)
        word = 'AREA'

        result = code_map.infer_new_key_from_word(sequence, word)

        self.assertEqual(result, CodeMap({1: 'A', 2: 'O', 3: 'R', 4: 'E'}))
