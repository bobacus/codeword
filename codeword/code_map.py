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

    def apply_to(self, sequences: list):
        key = self.key
        result = list()
        for s in sequences:
            result.append(tuple([c if c not in key else key[c] for c in s]))
        return result

    def infer_new_key_from_word(self, sequence: tuple, word: str):
        if len(sequence) != len(word):
            raise ValueError('lengths must match')
        key = dict(self.key)
        for i in range(0, len(sequence)):
            if isinstance(sequence[i], int):
                if sequence[i] in key:
                    if key[sequence[i]] != word[i]:
                        raise ValueError(
                            'sequence, word and key are inconsistent (%s, %s, %s)'
                            % (sequence, word, key))
                elif word[i] not in key.values():
                    key[sequence[i]] = word[i]
                else:
                    raise ValueError(
                        'sequence, word and key are inconsistent (%s, %s, %s)' % (sequence, word, key))
        return CodeMap(key)
