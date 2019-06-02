import unittest
from unittest.mock import patch

import codeword
from codeword.code_map import CodeMap
from codeword.grid import Grid


@patch('codeword.solver.solve', autospec=True, return_value=(Grid([[]]), None))
@patch('codeword.loaders.load_word_list', autospec=True)
@patch('codeword.loaders.load_map', autospec=True)
@patch('codeword.loaders.load_grid', autospec=True)
class TestMain(unittest.TestCase):
    def test_loads_grid(self, mock_load_grid, *_):
        grid_filename = 'grid.csv'

        codeword.main(grid_filename, 'map', 'word_list')

        mock_load_grid.assert_called_with(grid_filename)

    def test_loads_map(self, _1, mock_load_map, *_):
        map_filename = 'map.json'

        codeword.main('grid', map_filename, 'word_list')

        mock_load_map.assert_called_with(map_filename)

    def test_solves_codeword(self, mock_load_grid, mock_load_map, mock_load_word_list, mock_solve):
        grid = Grid([])
        code_map = CodeMap({})
        word_list = set()

        mock_load_grid.return_value = grid
        mock_load_map.return_value = code_map
        mock_load_word_list.return_value = word_list

        codeword.main('grid', 'map', 'word_list')

        mock_solve.assert_called_with(grid, code_map, word_list)
