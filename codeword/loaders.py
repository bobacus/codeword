from . import file
from .code_map import CodeMap
from .grid import Grid


def load_grid(filename: str):
    grid_data = file.load_csv(filename)
    cells = []
    for data_row in grid_data:
        cell_row = []
        for data_cell in data_row:
            try:
                cell = int(data_cell)
            except ValueError:
                cell = None
            cell_row.append(cell)
        cells.append(cell_row)
    return Grid(cells)


def load_map(filename: str):
    key_data = file.load_json(filename)
    key = {int(k): v for (k, v) in key_data.items()}
    return CodeMap(key)


def load_word_list(filename: str):
    word_list = file.load_csv(filename)
    return set(word_list)
