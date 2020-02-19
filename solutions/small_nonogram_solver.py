"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""

import functools


class Nonogram:

    def __init__(self, clues):
        self.clues = clues
        self.nonogram = [['?',] * len(self.clues[0]),][:] * len(self.clues[1])
        self.num_cols = len(self.clues[0])

    def solve(self):
        cols = common_positions(self.clues[0])
        cols = transpose_bitwise(cols)
        print('\ncols:')
        visualize(cols)
        rows = common_positions(self.clues[1])
        print('\nrows:')
        visualize(rows)
        self.ints_to_arr(combine(rows, cols))
        print('\nnonogram:')
        for line in self.nonogram:
            print(line)
        visualize(combine(rows, cols))
        return self.nonogram


    def ints_to_arr(self, int_nonogram):
        fmt = '{0:0' + str(self.num_cols) + 'b}'
        for row, item in enumerate(int_nonogram):
            for col, cell in enumerate(fmt.format(item)):
                self.nonogram[row][col] = cell if cell == '1' else self.nonogram[row][col]


def common_positions(clues):
    max_len = len(clues)
    items = []
    for clue in clues:
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        clue_shftd = init_shift(clue, max_len)
        positions = get_combinations(clue_shftd, 0, 0, max_r_shift)
        common_squares = and_merge(positions)
        items.append(common_squares)
    return items


def init_shift(squares, max_len):
    start_pos = 0
    squares_shftd = []
    for run in squares:
        shift = max_len - start_pos - run
        squares_shftd.append((2 ** run - 1) << shift)
        start_pos = start_pos + run + 1
    return squares_shftd


def or_merge(items):
    return functools.reduce(lambda x, y: x | y, items)


def and_merge(items):
    return functools.reduce(lambda x, y: x & y, items)


def transpose(items, max_len):
    items_transposed = []
    fmt = '{0:0' + str(max_len) + 'b}'
    for idx in range(max_len):
        transposed = [fmt.format(item)[idx] for item in items]
        transposed = int('0b' + ''.join(transposed), base=2)
        items_transposed.append(transposed)
    return items_transposed


def transpose_bitwise(items):
    max_len = len(items)
    items_transposed = []
    no_items = len(items)
    for idx in reversed(range(max_len)):
        transposed = sum([((item & (1 << idx)) >> idx) << (no_items - pos - 1)
                          for pos, item in enumerate(items)])
        items_transposed.append(transposed)
    return items_transposed


def combine(rows, cols):
    return [row | cols[idx] for idx, row in enumerate(rows)]


def visualize(items):
    max_len = len(items)
    fmt = '{0:0' + str(max_len) + 'b}'
    for item in items:
        print(f'{fmt.format(item)}')


def get_combinations(squares, idx, start_r_shift, max_r_shift):
    positions = []
    squares_shftd = squares[:]
    for r_shift in range(start_r_shift, max_r_shift + 1):
        squares_shftd[idx] = squares[idx] >> r_shift
        if idx < (len(squares) - 1):
            positions += get_combinations(squares_shftd, idx + 1, r_shift,
                                          max_r_shift)
        else:
            positions.append(or_merge(squares_shftd))
    return positions


def set_zeros(nonogram_ones):
    return


if __name__ == '__main__':
    clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
             ((1,), (2,), (3,), (2, 1), (4,)))
    ans = ((0, 0, 1, 0, 0),
           (1, 1, 0, 0, 0),
           (0, 1, 1, 1, 0),
           (1, 1, 0, 1, 0),
           (0, 1, 1, 1, 1))
    sol = Nonogram(clues).solve()
    print()
