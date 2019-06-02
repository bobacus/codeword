import unittest
from unittest.mock import patch

import codeword.loaders
from codeword.grid import Grid

@patch('codeword.file.load_csv', autospec=True)
class TestLoadGrid(unittest.TestCase):
    def test_reads_file_as_csv(self, mock_load_csv):
        filename = 'filename_7.csv'

        codeword.loaders.load_grid(filename)

        mock_load_csv.assert_called_with(filename)

    def test_creates_grid(self, mock_load_csv):
        grid_data = [
            ['x', '26', 'x'],
            ['5', '22', '6'],
            ['x', '21', 'x'],
        ]
        expected_grid = Grid([
            [None, 26, None],
            [5, 22, 6],
            [None, 21, None],
        ])

        mock_load_csv.return_value = grid_data

        grid = codeword.loaders.load_grid('filename_23.csv')

        self.assertEqual(grid, expected_grid)
