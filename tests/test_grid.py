import unittest

from code_map import CodeMap
from codeword.grid import Grid, transpose

class TestGrid(unittest.TestCase):
    def test_repr_0(self):
        grid = Grid([[]])

        self.assertEqual(repr(grid), 'Grid([[]])')

    def test_repr_1x1(self):
        grid = Grid([[1]])

        self.assertEqual(repr(grid), 'Grid([[1]])')

    def test_repr_2x2(self):
        grid = Grid([[2, None], [None, 3]])

        self.assertEqual(repr(grid), 'Grid([[2, None], [None, 3]])')

    def test_eq_0_0(self):
        a = Grid([])
        b = Grid([])

        self.assertEqual(a, b)

    def test_eq_0_1(self):
        a = Grid([])
        b = Grid([1])

        self.assertNotEqual(a, b)

    def test_str_0(self):
        self.assertEqual(str(Grid([[]])), '')

    def test_str_1(self):
        grid = Grid([[1]])
        self.assertEqual(str(grid), ' 1')

    def test_str_2x2(self):
        grid = Grid([[1, 2], [3, 4]])
        self.assertEqual(str(grid), ' 1  2\n 3  4')

    def test_str_3x3(self):
        grid = Grid([
            [None, 26, None],
            [5, 22, 6],
            [None, 21, None],
        ])
        self.assertEqual(str(grid), '   26   \n 5 22  6\n   21   ')

    def test_str_3x3_subst(self):
        grid = Grid([
            [None, 1, None],
            [2, 'R', 'E'],
            [None, 'E', None],
        ])
        self.assertEqual(str(grid), '    1   \n 2  R  E\n    E   ')

    def test_apply_key(self):
        grid = Grid([[1]])
        key = CodeMap({1: 'A'})

        result = grid.apply_key(key)

        self.assertEqual(result, Grid([['A']]))

    def test_sequences_0(self):
        grid = Grid([[]])
        self.assertEqual(grid.sequences(), set())

    def test_sequences_1(self):
        grid = Grid([['A']])
        self.assertEqual(grid.sequences(), {('A',)})

    def test_sequences_1_black(self):
        grid = Grid([[None]])
        self.assertEqual(grid.sequences(), set())

    def test_sequences_2_ad(self):
        grid = Grid([['A', None], [None, 'D']])
        self.assertEqual(grid.sequences(), {('A',), ('D',)})

    def test_sequences_2_bc(self):
        grid = Grid([[None, 'B'], ['C', None]])
        self.assertEqual(grid.sequences(), {('B',), ('C',)})

    def test_sequences_2_abc(self):
        grid = Grid([['A', 'B'], ['C', None]])
        self.assertEqual(grid.sequences(), {('A', 'B'), ('A', 'C')})


class TestTranspose(unittest.TestCase):
    def test_transpose_0(self):
        cells = [[]]
        self.assertEqual(transpose(cells), [[]])
