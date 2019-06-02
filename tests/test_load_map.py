import unittest
from unittest.mock import patch

import codeword.loaders
from codeword.code_map import CodeMap


@patch('codeword.file.load_json', autospec=True)
class TestLoadMap(unittest.TestCase):
    def test_reads_file_as_json(self, mock_load_json):
        filename = 'filename_10.json'

        codeword.loaders.load_map(filename)

        mock_load_json.assert_called_with(filename)

    def test_creates_map(self, mock_load_json):
        mock_load_json.return_value = {
            '2': 'T',
            '9': 'P',
            '17': 'E',
        }
        expected_map = CodeMap({
            2: 'T',
            9: 'P',
            17: 'E',
        })

        code_map = codeword.loaders.load_map('map_28.json')

        self.assertEquals(code_map, expected_map)
