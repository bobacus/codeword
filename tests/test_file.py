import unittest
from unittest.mock import patch, mock_open

from codeword import file

test_csv_data = '''foo,bar,12
,,x'''

@patch('builtins.open', new_callable=mock_open, read_data=test_csv_data)
class TestLoadCsv(unittest.TestCase):
    def test_opens_file(self, mock_file_open):
        filename = 'csv_file_9.csv'

        file.load_csv(filename)

        mock_file_open.assert_called_with(filename, newline='')

    def test_parses_csv_data(self, *_):
        data = file.load_csv('csv_file_17.csv')

        self.assertEqual(
            data,
            [
                ['foo', 'bar', '12'],
                ['', '', 'x'],
            ])

test_json_data = '''{"a": "b",
"c":    "d"}'''

@patch('builtins.open', new_callable=mock_open, read_data=test_json_data)
class TestLoadJson(unittest.TestCase):
    def test_opens_file(self, mock_file_open):
        filename = 'file_37.json'

        file.load_json(filename)

        mock_file_open.assert_called_with(filename)

    def test_parses_json_data(self, *_):
        data = file.load_json('file_42.json')

        self.assertEqual(
            data,
            {'a': 'b', 'c': 'd'})
