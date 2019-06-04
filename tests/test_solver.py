import unittest

from codeword import solver
from codeword.code_map import CodeMap
from codeword.grid import Grid


class TestSolver(unittest.TestCase):
    def test_populates_grid_from_map(self):
        word_list = {
            'A',
            'ARE',
            'AREA',
            'OR',
            'ORE',
            'RARE',
            'REAR',
            'ROAR',
        }
        initial_grid = Grid([
            [None, 1, None],
            [2, 3, 4],
            [None, 4, None],
            [None, 1, None],
        ])
        initial_key = CodeMap({3: 'R', 4: 'E'})

        grid, key = solver.solve(initial_grid, initial_key, word_list)

        self.assertEqual(key, CodeMap({1: 'A', 2: 'O', 3: 'R', 4: 'E'}))
        self.assertEqual(grid, Grid([
            [None, 'A', None],
            ['O', 'R', 'E'],
            [None, 'E', None],
            [None, 'A', None],
        ]))

    word_list = {
        'A',
        'AS',
        'ASS',
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
        sequences = [
            (1,),
            (1, 2),
            (3, 1, 2),
            (1, 3),
        ]

        result = solver.solve_sequences(key, sequences, {s: self.word_list for s in sequences})

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

    def test_word_matches_12_XX_false(self):
        self.assertFalse(solver.word_matches((1, 2), 'XX'))

    def test_word_matches_11_XY_false(self):
        self.assertFalse(solver.word_matches((1, 1), 'XY'))

    def test_word_matches_A1_AA_false(self):
        self.assertFalse(solver.word_matches(('A', 1), 'AA'))

    def test_find_possible_words(self):
        sequences = [
            ('A',),
            ('A', 2),
            (3, 'A', 2),
            ('A', 3),
        ]

        words = solver.find_possible_words(list(zip(sequences, [self.word_list for _ in sequences])))

        self.assertEqual(words, {
            sequences[0]: {'A'},
            sequences[1]: {'AS', 'AT'},
            sequences[2]: {'SAT'},
            sequences[3]: {'AS', 'AT'},
        })

    def test_find_possible_words_no_inconsistency(self):
        sequences_word_lists = [
            ((1, 2, 3), {'AAA', 'AAB', 'ABB', 'ABA', 'ABC', 'ACB', 'ACA', 'ACC'}),
        ]

        words = solver.find_possible_words(sequences_word_lists)

        self.assertEqual(words, {
            sequences_word_lists[0][0]: {'ABC', 'ACB'},
        })

    def test_find_possible_words_error_if_no_matching_word_for_sequence(self):
        sequences = [
            ((1, 2, 1), {'CAT'}),
        ]

        with self.assertRaises(ValueError):
            solver.find_possible_words(sequences)

    def test_sort_sequences_0(self):
        sequences = []

        result = solver.sort_sequences(sequences)

        self.assertEqual(result, [])

    def test_sort_sequences_kk(self):
        sequences = [
            ('A', 'B')
        ]

        result = solver.sort_sequences(sequences)

        self.assertEqual(result, [('A', 'B')])

    def test_sort_sequences_kk_kk(self):
        sequences = [
            ('B', 'C'),
            ('A', 'B'),
        ]

        result = solver.sort_sequences(sequences)

        self.assertEqual(result, [('B', 'C'), ('A', 'B')])

    def test_sort_sequences_uk_uk(self):
        sequences = [
            (1, 'C'),
            (2, 'B'),
        ]

        result = solver.sort_sequences(sequences)

        self.assertEqual(result, [(1, 'C'), (2, 'B')])

    def test_sort_sequences_ku_uk(self):
        sequences = [
            ('A', 1),
            (2, 'B'),
        ]

        result = solver.sort_sequences(sequences)

        self.assertEqual(result, [('A', 1), (2, 'B')])

    def test_sort_sequences_ku_kk(self):
        sequences = [
            ('A', 1),
            ('A', 'B'),
        ]

        result = solver.sort_sequences(sequences)

        self.assertEqual(result, [('A', 'B'), ('A', 1)])

    def test_sort_sequences_ku_kkk(self):
        sequences = [
            ('A', 1),
            ('B', 'C', 'D'),
        ]

        result = solver.sort_sequences(sequences)

        self.assertEqual(result, [('B', 'C', 'D'), ('A', 1)])

    def test_sort_sequences_unique_unknowns_trump(self):
        sequences = [
            (2, 1),
            (2, 2),
        ]

        result = solver.sort_sequences(sequences)

        self.assertEqual(result, [(2, 2), (2, 1)])

    def test_hash_sequence(self):
        sequence = ('A', 1)

        self.assertEqual(solver.hash_sequence(sequence), hash('A.'))

    def test_hash_function_sequence(self):
        sequence = ('A', 1)

        fn = solver.hash_function(sequence)

        self.assertEqual(fn(sequence), hash('A.'))

    def test_hash_function_word(self):
        sequence = ('A', 1)
        word = 'AB'

        fn = solver.hash_function(sequence)

        self.assertEqual(fn(word), hash('A.'))

    def test_hash_function_zero_for_differing_lengths(self):
        sequence = ('A', 1)
        word = 'B'

        fn = solver.hash_function(sequence)

        self.assertEqual(fn(word), 0)
