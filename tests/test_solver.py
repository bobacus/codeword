import unittest

from codeword import solver
from codeword.code_map import CodeMap
from codeword.grid import Grid


class TestSolver(unittest.TestCase):
    def test_populates_grid_from_map(self):
        word_list = {
            'ARE',
            'ORE',
        }
        initial_grid = Grid([
            [None, 1, None],
            [2, 3, 4],
            [None, 4, None],
        ])
        initial_key = CodeMap({3: 'R', 4: 'E'})

        grid, key = solver.solve(initial_grid, initial_key, word_list)

        self.assertEqual(key, CodeMap({1: 'A', 2: 'O', 3: 'R', 4: 'E'}))
        self.assertEqual(grid, Grid([
            [None, 'A', None],
            ['O', 'R', 'E'],
            [None, 'E', None],
        ]))

    word_list = {
        'A',
        'AS',
        'AT',
        'I',
        'IS',
        'IT',
        'ITS',
        'SAT',
        'SIT',
        'SITS',
    }

    def test_solve_sequences(self):
        key = CodeMap({1: 'A'})
        sequences = {
            (1,),
            (1, 2),
            (3, 1, 2),
            (1, 3),
        }

        result = solver.solve_sequences(key, sequences, self.word_list)

        self.assertEqual(result, CodeMap({
            1: 'A',
            2: 'T',
            3: 'S',
        }))

    def test_word_matches_1_any(self):
        self.assertTrue(solver.word_matches((12,), 'x'))

    def test_word_matches_1_X(self):
        self.assertTrue(solver.word_matches(('X',), 'X'))

    def test_word_matches_1_X_false(self):
        self.assertFalse(solver.word_matches(('X',), 'Y'))

    def test_find_possible_words(self):
        sequences = {
            ('A',),
            ('A', 2),
            (3, 'A', 2),
            ('A', 3),
        }

        words = solver.find_possible_words(sequences, self.word_list)

        self.assertEqual(words, {
            'A',
            'AS',
            'AT',
            'SAT',
        })