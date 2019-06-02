import unittest

from codeword.cursor import Cursor

class TestCursor(unittest.TestCase):
    def test_initial_position(self):
        cursor = Cursor([[]])
        self.assertEqual(cursor.position, (0, 0))

    def test_read_value(self):
        cursor = Cursor([[1]])
        self.assertEqual(cursor.read(), 1)

    def test_read_value_x_y(self):
        cursor = Cursor([[1], [2]])
        cursor.advance_row()
        self.assertEqual(cursor.read(), 2)

    def test_read_out_of_range(self):
        cursor = Cursor([[]])
        self.assertIsNone(cursor.read())

    def test_beyond_fence_0_negative(self):
        cursor = Cursor([[]])
        self.assertFalse(cursor.beyond_fence())

    def test_beyond_fence_0_positive(self):
        cursor = Cursor([[]])
        cursor.advance()
        self.assertTrue(cursor.beyond_fence())

    def test_beyond_fence_1_negative(self):
        cursor = Cursor([[1]])
        cursor.advance()
        self.assertFalse(cursor.beyond_fence())

    def test_beyond_fence_1_positive(self):
        cursor = Cursor([[1]])
        cursor.advance()
        cursor.advance()
        self.assertTrue(cursor.beyond_fence())

    def test_advance(self):
        cursor = Cursor([[1]])
        cursor.advance()
        self.assertEqual(cursor.position, (1, 0))

    def test_has_more_rows_positive(self):
        cursor = Cursor([[1]])
        self.assertTrue(cursor.has_more_rows())

    def test_has_more_rows_negative(self):
        cursor = Cursor([[1]])
        cursor.advance_row()
        self.assertTrue(cursor.has_more_rows())

    def test_advance_row(self):
        cursor = Cursor([[]])
        cursor.advance_row()
        self.assertEqual(cursor.position, (0, 1))

    def test_find_sequences_2_abc(self):
        cursor = Cursor([['A', 'B'], ['C', None]])
        self.assertEqual(cursor.find_sequences(), {('A', 'B')})

    def test_find_sequences_2_abd(self):
        cursor = Cursor([['A', 'B'], [None, 'D']])
        self.assertEqual(cursor.find_sequences(), {('A', 'B')})

    def test_find_sequences_2_bcd(self):
        cursor = Cursor([[None, 'B'], ['C', 'D']])
        self.assertEqual(cursor.find_sequences(), {('C', 'D')})

    def test_satisfies_single_letter_rule_2_abc_11(self):
        cursor = Cursor([['A', 'B'], ['C', None]])
        cursor._position = (1, 1)
        self.assertFalse(cursor.satisfies_single_letter_rule(['C']))

    def test_satisfies_single_letter_rule_2_abc_20(self):
        cursor = Cursor([['A', 'B'], ['C', None]])
        cursor._position = (2, 0)
        self.assertTrue(cursor.satisfies_single_letter_rule(['A', 'B']))

    def test_satisfies_single_letter_rule_2_bcd_20(self):
        cursor = Cursor([['A', 'B'], [None, 'D']])
        cursor._position = (2, 0)
        self.assertFalse(cursor.satisfies_single_letter_rule(['B']))

    def test_satisfies_single_letter_rule_2_ad_10(self):
        cursor = Cursor([['A', None], [None, 'D']])
        cursor._position = (1, 0)
        self.assertTrue(cursor.satisfies_single_letter_rule(['A']))

    def test_read_northwest_value(self):
        cursor = Cursor([['A']])
        cursor._position = (1, 1)
        self.assertEqual(cursor.read(-1, -1), 'A')

    def test_read_northwest_out_of_bounds(self):
        cursor = Cursor([['A']])
        cursor._position = (0, 0)
        self.assertIsNone(cursor.read(-1, -1))
