class Cursor:

    def __init__(self, cells):
        if not isinstance(cells, list):
            raise TypeError('cells must be a list')
        if len(cells) < 1:
            raise ValueError('cells must have at least one element')
        if not isinstance(cells[0], list):
            raise TypeError('cells must be a list of lists')

        self._cells = cells
        self._position = (0, 0)

    @property
    def position(self) -> tuple:
        return self._position

    def read(self, rel_x=0, rel_y=0):
        x = self.position[0] + rel_x
        y = self.position[1] + rel_y
        if x < 0 or y < 0:
            return None
        try:
            return self._cells[y][x]
        except IndexError:
            return None

    def beyond_fence(self):
        return self._position[0] > len(self._cells[0])

    def advance(self):
        self._position = (self._position[0] + 1, self._position[1])

    def advance_row(self):
        self._position = (0, self._position[1] + 1)

    def has_more_rows(self):
        return self._position[1] <= len(self._cells)

    def find_sequences(self):
        result = set()
        while self.has_more_rows():
            s = []
            while not self.beyond_fence():
                value = self.read()
                if value:
                    s.append(value)
                else:
                    if s and self.satisfies_single_letter_rule(s):
                        result.add(tuple(s))
                    s = []
                self.advance()
            self.advance_row()
        return result

    def satisfies_single_letter_rule(self, sequence):
        if len(sequence) == 1:
            return not self.read(-1, -1) and not self.read(-1, 1)
        return True
