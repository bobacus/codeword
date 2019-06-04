from sys import stderr

from .code_map import CodeMap
from .grid import Grid


def solve(initial_grid: Grid, initial_map: CodeMap, word_list: set):
    grid = initial_grid.apply_key(initial_map)

    sequences = grid.sequences()
    key = solve_sequences(initial_map, sequences, word_list)
    grid = grid.apply_key(key)

    return grid, key


def solve_sequences(code_map: CodeMap, sequences: list, word_list: set):
    # print('solve_sequences [%s] [%s] [%s]' % (code_map, sequences, word_list), file=stderr)
    print('solve_sequences: [%s] len(word_list) = %s' % (code_map, len(word_list)), file=stderr, flush=True)
    sequences = code_map.apply_to(sequences)
    # print('sequences now [%s]' % sequences, file=stderr)
    if is_complete_and_valid(sequences, word_list):
        return code_map

    possible_words = find_possible_words(sequences, word_list)

    for sequence in sort_sequences(sequences):
        # print('sequence: %s' % str(sequence), file=stderr, flush=True)
        if is_complete(sequence):
            continue
        matching_words = find_possible_words([sequence], possible_words)
        # print('matching_words: %s' % matching_words, file=stderr)
        if not matching_words:
            raise ValueError('no more words - inconsistent map / set / word-list')
        for word in matching_words:
            # print('trying word [%s]' % word, file=stderr)
            try:
                new_map = code_map.infer_new_key_from_word(sequence, word)
                return solve_sequences(new_map, sequences, possible_words)
            except ValueError:
                pass

    raise ValueError('inconsistent map, set, word-list')


def is_complete_and_valid(sequences, word_list):
    for s in sequences:
        if not is_complete(s):
            return False
        word = ''.join(s)
        if word not in word_list:
            raise ValueError('completed sequence [%s] not in word list' % word)
    return True


def is_complete(sequence):
    for c in sequence:
        if isinstance(c, int):
            return False
    return True


def find_possible_words(sequences: list, word_list: set):
    result = set()
    for s in sequences:
        possible_words = set()
        for w in word_list:
            if word_matches(s, w):
                possible_words.add(w)
        if not possible_words:
            raise ValueError('no matching words for sequence [%s]' % str(s))
        result |= possible_words
    return result


def word_matches(sequence: tuple, word: str):
    if len(sequence) != len(word):
        return False
    memo_key = {}
    memo_plain = {}
    for i in range(0, len(sequence)):
        if isinstance(sequence[i], str):
            if word[i] != sequence[i]:
                return False
        if sequence[i] in memo_key:
            if word[i] != memo_key[sequence[i]]:
                return False
        if word[i] in memo_plain:
            if sequence[i] != memo_plain[word[i]]:
                return False
        memo_key[sequence[i]] = word[i]
        memo_plain[word[i]] = sequence[i]
    return True


def sort_sequences(sequences: list) -> list:
    return sorted(sequences, key=lambda x: sum(1 for y in set(x) if isinstance(y, int)))
