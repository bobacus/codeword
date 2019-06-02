from .code_map import CodeMap
from .grid import Grid


def solve(initial_grid: Grid, initial_map: CodeMap, word_list: set):
    grid = initial_grid.apply_key(initial_map)

    sequences = grid.sequences()
    key = solve_sequences(initial_map, sequences, word_list)

    return grid, key


def solve_sequences(code_map: CodeMap, sequences: set, word_list: set):
    if code_map.is_complete():
        return code_map

    partial_sequences = code_map.apply_to(sequences)
    possible_words = find_possible_words(partial_sequences, word_list)



    return CodeMap({})


def find_possible_words(sequences: set, word_list: set):
    possible_words = set()
    for s in sequences:
        for w in word_list:
            if word_matches(s, w):
                possible_words.add(w)
    return possible_words


def word_matches(sequence: tuple, word: str):
    if len(sequence) != len(word):
        return False
    for i in range(0, len(sequence)):
        if isinstance(sequence[i], str):
            if word[i] != sequence[i]:
                return False
    return True
