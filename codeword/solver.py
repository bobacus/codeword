from sys import stderr

from .code_map import CodeMap
from .grid import Grid


def solve(initial_grid: Grid, initial_map: CodeMap, word_list: set):
    grid = initial_grid.apply_key(initial_map)

    sequences = grid.sequences()
    key = solve_sequences(initial_map, sequences, {s: word_list for s in sequences})
    grid = grid.apply_key(key)

    return grid, key


def solve_sequences(code_map: CodeMap, orig_sequences: list, word_lists: dict):
    # print('solve_sequences [%s] [%s] [%s]' % (code_map, orig_sequences, word_list), file=stderr)
    word_count = sum(len(l) for l in word_lists.values())
    print(
        'solve_sequences: [%s] sum(len(word_lists)) = %s' % (code_map, word_count),
        file=stderr,
        flush=True)
    sequences = code_map.apply_to(orig_sequences)
    # print('sequences now [%s]' % sequences, file=stderr)

    complete_and_valid = True
    for i in range(0, len(sequences)):
        if not is_complete_and_valid(sequences[i], word_lists[orig_sequences[i]]):
            complete_and_valid = False
            break
    if complete_and_valid:
        return code_map

    sequence_word_lists = find_possible_words(list(zip(sequences, [word_lists[s] for s in orig_sequences])))

    for sequence in sort_sequences(sequences):
        # print('sequence: %s' % str(sequence), file=stderr, flush=True)
        if is_complete(sequence):
            continue

        matching_words = sequence_word_lists[sequence]
        # print('matching_words: %s' % matching_words, file=stderr)
        if not matching_words:
            raise ValueError('no more words - inconsistent map / set / word-list')

        for word in matching_words:
            try:
                new_map = code_map.infer_new_key_from_word(sequence, word)
                new_word_lists = {**sequence_word_lists, sequence: {word}}
                print('[{:<13}] '.format(word), file=stderr, end='')
                return solve_sequences(new_map, sequences, new_word_lists)
            except ValueError:
                pass

    raise ValueError('inconsistent map, set, word-list')


def is_complete_and_valid(sequence: tuple, word_list):
    if not is_complete(sequence):
        return False
    word = ''.join(sequence)
    if word not in word_list:
        raise ValueError('completed sequence [%s] not in word list' % word)
    return True


def is_complete(sequence):
    for c in sequence:
        if isinstance(c, int):
            return False
    return True


def find_possible_words(sequence_word_list_tuples: list):
    result = dict()
    for t in sequence_word_list_tuples:
        possible_words = set()
        sequence = t[0]
        word_list = t[1]
        hash_fn = hash_function(sequence)
        hash_s = hash_fn(sequence)
        for w in word_list:
            if hash_s == hash_fn(w):
                if word_matches(sequence, w):
                    possible_words.add(w)
        if not possible_words:
            raise ValueError('no matching words for sequence]')
        result[sequence] = possible_words
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


def hash_sequence(sequence):
    return hash_function(sequence)(sequence)


def hash_function(sequence):
    def f(value):
        if len(sequence) != len(value):
            return 0
        s = ''
        for i in range(0, len(sequence)):
            if isinstance(sequence[i], int) or isinstance(value[i], int):
                s += '.'
            else:
                s += value[i]
        return hash(s)
    return f
