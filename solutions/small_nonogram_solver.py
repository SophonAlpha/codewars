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
        self.nonogram_ones = [0,] * len(self.row_clues)
        self.nonogram_zeros = [0,] * len(self.row_clues)
        self.num_cols = len(self.col_clues)

    def solve(self):
        while not self.is_solved():
            self.show()
            print()
            t_ones = transpose_bitwise(self.nonogram_ones)
            t_zeros = transpose_bitwise(self.nonogram_zeros)
            col_pos_masks = [~(t_ones[idx] | t_zeros[idx])
                             for idx, _ in enumerate(t_ones)]
            cols = common_positions(self.col_clues, col_pos_masks)
            cols = transpose_bitwise(cols)
            row_pos_marks = col_pos_masks[:]
            rows = common_positions(self.row_clues, row_pos_marks)
            self.set_ones(rows, cols)
            self.show()
            print()
            self.set_zeros()
            self.show()

    def is_solved(self):
        mask = 2**len(self.col_clues) - 1
        for idx in range(len(self.row_clues)):
            if mask & (self.nonogram_ones[idx] | self.nonogram_zeros[idx]) != mask:
                return False
        return True

    def set_ones(self, rows, cols):
        self.nonogram_ones = combine(rows, cols)

    def set_zeros(self):
        num_cols = len(self.col_clues)
        for col, col_clues in enumerate(self.col_clues):
            mask = 1 << col
            nono_col_sum = sum([(item & mask) >> num_cols - 2
                                for item in self.nonogram_ones])
            if nono_col_sum == sum(col_clues):
                for row in self.nonogram_ones:
                    if self.nonogram_ones[row] & mask != mask:
                        self.nonogram_zeros[row] |= mask
        for row, row_clues in enumerate(self.row_clues):
            nono_row_sum = bin(self.nonogram_ones[row])[2:].count('1')
            if nono_row_sum == sum(row_clues):
                self.nonogram_zeros[row] = self.nonogram_ones[row] ^ (2 ** num_cols - 1)

    def show(self):
        # transform binary representation to list of string representation
        self.nonogram = transform_bin2str(self.nonogram,
                                          self.nonogram_ones,
                                          self.nonogram_zeros)
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


def transform_bin2str(nonogram, nonogram_ones, nonogram_zeros):
    num_cols = len(nonogram[0])
    fmt = '{0:0' + str(num_cols) + 'b}'
    for row, item in enumerate(nonogram_ones):
        for col, cell in enumerate(fmt.format(item)):
            nonogram[row][col] = cell if cell == '1' \
                else nonogram[row][col]
    for row, item in enumerate(nonogram_zeros):
        for col, cell in enumerate(fmt.format(item)):
            nonogram[row][col] = '0' if cell == '1' \
                else nonogram[row][col]
    return nonogram


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


def common_positions(clues, pos_masks):
    items = []
    for common_positions in combinations(clues, pos_masks):
        items.append(common_positions)
    return items


def combinations(clues, pos_masks):
    max_len = len(clues)
    for clue in clues:
        common_positions = None
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
                if common_positions == 0:
                    break
        yield common_positions


def combinator(clue, idx, start_r_shift, max_r_shift):
    clue_shftd = clue[:]
    for r_shift in range(start_r_shift, max_r_shift + 1):
        clue_shftd[idx] = clue[idx] >> r_shift
        if idx < (len(clue) - 1):
            yield from combinator(clue_shftd, idx + 1, r_shift, max_r_shift)
        else:
            yield clue_shftd


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
