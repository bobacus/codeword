from .code_map import CodeMap
from .cursor import Cursor


def transpose(m):
    if len(m) == 0 or len(m[0]) == 0:
        return [[]]
    return list(map(list, zip(*m)))

class Grid:
    def __init__(self, cells):
        self.cells = cells

    def __repr__(self):
        return 'Grid(%r)' % self.cells

    def __eq__(self, other):
        return self.cells == other.cells

    def __str__(self):
        lines = [' '.join('{:>2}'.format(c) if c else '  ' for c in l) for l in self.cells]
        return '\n'.join(lines)

    def apply_key(self, code_map: CodeMap):
        key = code_map.key
        return Grid([[c if c not in key else key[c] for c in row] for row in self.cells])

    def sequences(self):
        result = set()

        cursor = Cursor(self.cells)
        result |= cursor.find_sequences()

        cursor = Cursor(transpose(self.cells))
        result |= cursor.find_sequences()

        return result
