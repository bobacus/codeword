from . import loaders, solver


def main(grid_filename: str, map_filename: str, word_list_filename: str):
    initial_grid = loaders.load_grid(grid_filename)
    initial_map = loaders.load_map(map_filename)
    word_list = loaders.load_word_list(word_list_filename)
    solved_grid, solved_map = solver.solve(initial_grid, initial_map, word_list)

    print('GRID')
    print(solved_grid)
    print()

    print('KEY')
    print(solved_map)
    print()

    print('SEQUENCES')
    print(format_sequences(solved_grid.sequences()))


def format_sequences(sequences: set):
    lines = []
    for sequence in sequences:
        lines.append(''.join([c if isinstance(c, str) else '.' for c in sequence]))
    return '\n'.join(lines)
