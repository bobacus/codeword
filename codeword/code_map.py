class CodeMap:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __repr__(self):
        return 'CodeMap(%r)' % self.key

    def __str__(self):
        o = list('.' * 26)
        for code in self.key:
            o[code - 1] = self.key[code]
        return ''.join(o)

    def apply_to(self, sequences: set):
        key = self.key
        return [[c if c not in key else key[c] for c in s] for s in sequences]
