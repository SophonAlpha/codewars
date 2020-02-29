"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""

import functools


class Nonogram:

    def __init__(self, clues):
        self.col_clues, self.row_clues = clues[0], clues[1]
        self.nonogram = [['?',] * len(self.col_clues) for _ in self.row_clues]
        self.nonogram_ones = 0
        self.nonogram_zeros = 0
        self.num_cols = len(self.col_clues)

    def solve(self):
        cols = common_positions(self.col_clues)
        cols = transpose_bitwise(cols)
        rows = common_positions(self.row_clues)
        self.set_ones(combine(rows, cols))
        self.show()
        print()
        self.set_zeros()
        self.show()

    def set_ones(self, int_nonogram):
        fmt = '{0:0' + str(self.num_cols) + 'b}'
        for row, item in enumerate(int_nonogram):
            for col, cell in enumerate(fmt.format(item)):
                self.nonogram[row][col] = cell if cell == '1' \
                    else self.nonogram[row][col]

    def set_zeros(self):
        for col, col_clues in enumerate(self.col_clues):
            nono_col_sum = sum([1 if row[col] == '1' else 0
                                for row in self.nonogram])
            if nono_col_sum == sum(col_clues):
                for row, _ in enumerate(self.nonogram):
                    if self.nonogram[row][col] == '?':
                        self.nonogram[row][col] = '0'

        for row, row_clues in enumerate(self.row_clues):
            nono_row_sum = sum([1 if col == '1' else 0
                                for col in self.nonogram[row]])
            if nono_row_sum == sum(row_clues):
                for col, _ in enumerate(self.nonogram[row]):
                    if self.nonogram[row][col] == '?':
                        self.nonogram[row][col] = '0'

    def show(self):
        # transform column clues
        col_clues = transform_col_clues(self.col_clues)
        # transform row clues
        row_clues_strs = transform_row_clues(self.row_clues)
        nonogram_view = [' ' * (len(row_clues_strs[0]) + 1) + line
                         for line in col_clues]
        for idx, row in enumerate(self.nonogram):
            nonogram_view.append(
                row_clues_strs[idx] + '|' + '|'.join([' ' + item + ' '
                                                      for item in row]) + '|'
            )
        # print nonogram
        for line in nonogram_view:
            print(line)


def transform_col_clues(clues):
    col_clues_rows = max([len(clue) for clue in clues])
    col_clues = clues[:]
    col_clues = [(0,) * (col_clues_rows - len(item)) + item
                 for item in col_clues]
    col_clues = zip(*[item for item in col_clues])
    col_clues = [[str(item) if item != 0 else ' '
                  for item in line] for line in col_clues]
    col_clues = [' '.join([str(item).rjust(2, ' ') + ' ' for item in line])
                 for line in col_clues]
    return col_clues


def transform_row_clues(clues):
    row_clues = [', '.join([str(item) for item in clue])
                 for clue in clues]
    row_clue_max = max([len(item) for item in row_clues])
    row_clues = [' ' * (row_clue_max - len(item)) + item + ' '
                 for item in row_clues]
    return row_clues


def common_positions(clues):
    items = []
    for common_positions in combinations(clues):
        items.append(common_positions)
    return items


def combinations(clues):
    common_positions = None
    max_len = len(clues)
    for clue in clues:
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        clue_shftd = init_shift(clue, max_len)
        for combination in combinator(clue_shftd, 0, 0, max_r_shift):
            if not common_positions:
                # store very first value
                common_positions = or_merge(combination)
            else:
                # bitwise 'and' with any subsequent value
                common_positions = and_merge([common_positions,
                                              or_merge(combination)])
                # TODO: here is a point for performance optimization.
                # If common_positions is zero after the and_merge then stop
                # the loop. There is no benefit in continuing as there
                # is no common position across all combinations.
        yield common_positions


"""
fmt.format(b)
Out[13]: '01001'
fmt.format(b ^ (2**5 - 1))
Out[14]: '10110'
fmt.format(b ^ (2**5 - 1) | 18)
Out[15]: '10110'
fmt.format((b ^ (2**5 - 1)) | 18)
Out[16]: '10110'
fmt.format((b ^ (2**5 - 1)) & 18)
Out[17]: '10010'
"""


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


def combinator(clue, idx, start_r_shift, max_r_shift):
    clue_shftd = clue[:]
    for r_shift in range(start_r_shift, max_r_shift + 1):
        clue_shftd[idx] = clue[idx] >> r_shift
        if idx < (len(clue) - 1):
            yield from combinator(clue_shftd, idx + 1, r_shift, max_r_shift)
        else:
            yield clue_shftd


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
