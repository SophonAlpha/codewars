"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""

import functools
import solutions.small_nonogram_solver_show as nshow


class Nonogram:

    def __init__(self, clues):
        self.col_clues, self.row_clues = clues[0], clues[1]
        self.col_clues = reorder(self.col_clues)
        self.nonogram = [['?', ] * len(self.col_clues) for _ in self.row_clues]
        self.nonogram_ones = [0, ] * len(self.row_clues)
        self.nonogram_zeros = [0, ] * len(self.row_clues)
        self.num_cols = len(self.col_clues)
        self.num_rows = len(self.row_clues)
        self.col_bit_mask = 2 ** self.num_cols - 1
        self.row_bit_mask = 2 ** self.num_rows - 1
        self.nonogram_col_masks = [self.col_bit_mask, ] * self.num_cols
        self.nonogram_row_masks = [self.row_bit_mask, ] * self.num_rows

    def solve(self):
        while not self.is_solved():
            self.show()
            print('\nset positions in columns')
            # set positions in columns
            col_pos_masks = self.get_col_masks()
            cols = common_positions(self.col_clues, col_pos_masks)
            cols = rows2cols(cols, len(cols))
            self.set_ones(cols)
            self.show()
            print('\nset the zeros')
            self.set_zeros()
            self.show()
            print('\nset positions in rows')
            self.update_nonogram_mask()
            # set positions in rows
            row_pos_masks = self.get_row_masks()
            rows = common_positions(self.row_clues, row_pos_masks)
            self.set_ones(rows)
            self.show()
            print('\nset the zeros')
            self.set_zeros()
            self.show()
            print()
            self.update_nonogram_mask()
        self.nonogram = transform_bin2str(self.nonogram,
                                          self.nonogram_ones,
                                          self.nonogram_zeros)
        nonogram_tuple = tuple(
            tuple(int(cell) for cell in row) for row in self.nonogram)
        return nonogram_tuple

    def is_solved(self):
        return sum(self.nonogram_row_masks) + sum(self.nonogram_col_masks) == 0

    def update_nonogram_mask(self):
        # combine ones & zeros with bitwise or the invert the mask
        ones_zeros = [
            ~(self.nonogram_ones[idx] | self.nonogram_zeros[idx])
            & self.col_bit_mask for idx, _ in enumerate(self.nonogram_ones)
        ]
        # row wise add all set positions ("1s")
        self.nonogram_row_masks = ones_zeros[:]
        self.nonogram_row_masks = [
            mask | self.nonogram_ones[idx] if mask != 0 else mask
            for idx, mask in enumerate(self.nonogram_row_masks)
        ]
        # column wise add all set positions ("1s")
        self.nonogram_col_masks = cols2rows(ones_zeros[:], self.num_cols)
        col_ones = cols2rows(self.nonogram_ones, self.num_cols)
        self.nonogram_col_masks = [
            mask | col_ones[idx] if mask != 0 else mask
            for idx, mask in enumerate(self.nonogram_col_masks)
        ]

    def get_col_masks(self):
        return self.nonogram_col_masks[:]

    def get_row_masks(self):
        return self.nonogram_row_masks[:]

    def set_ones(self, items):
        self.nonogram_ones = [self.nonogram_ones[idx] | item
                              for idx, item in enumerate(items)]

    def set_zeros(self):
        # TODO: Refactor code to reduce nesting depth.
        for col, col_clues in enumerate(self.col_clues):
            bit_pos = self.num_cols - col - 1
            mask = 1 << bit_pos
            nono_col_sum = sum([(item & mask) >> bit_pos
                                for item in self.nonogram_ones])
            if nono_col_sum == sum(col_clues):
                for idx, row in enumerate(self.nonogram_ones):
                    if row & mask != mask:
                        self.nonogram_zeros[idx] |= mask
        for row, row_clues in enumerate(self.row_clues):
            nono_row_sum = bin(self.nonogram_ones[row])[2:].count('1')
            if nono_row_sum == sum(row_clues):
                self.nonogram_zeros[row] = self.nonogram_ones[row] ^ (
                        2 ** self.num_cols - 1)

    def show(self):
        self.nonogram = transform_bin2str(self.nonogram,
                                          self.nonogram_ones,
                                          self.nonogram_zeros)
        reordered_col_clues = reorder(self.col_clues)
        nshow.show(self.nonogram, self.nonogram_ones, self.nonogram_zeros,
                   reordered_col_clues, self.row_clues)


def reorder(items):
    return tuple(tuple(item[::-1]) for item in items)


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
    items = [0 if item is None else item for item in items]
    return items


def combinations(clues, pos_masks):
    max_len = len(clues)
    # TODO: Refactor code to reduce deep nesting.
    for pos, clue in enumerate(clues):
        common_positions = None
        if pos_masks[pos] != 0:
            max_r_shift = max_len - (sum(clue) + len(clue) - 1)
            clue_shftd = init_shift(clue, max_len)
            for combination in combinator(clue_shftd, 0, 0, max_r_shift):
                combination = or_merge(combination)
                if combination & pos_masks[pos] == combination:
                    if not common_positions:
                        # store very first value
                        common_positions = combination
                    else:
                        # bitwise 'and' with any subsequent value
                        common_positions = and_merge(
                            [common_positions, combination])
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


def cols2rows(items, max_len):
    new_rows = []
    for idx in reversed(range(max_len)):
        new_rows.append(sum([((item & (1 << idx)) >> idx) << pos
                             for pos, item in enumerate(items)]))
    return new_rows


def rows2cols(items, max_len):
    new_cols = []
    for idx, _ in enumerate(items):
        new_cols.append(sum([((item & (1 << idx)) >> idx) << (max_len - pos - 1)
                             for pos, item in enumerate(items)]))
    return new_cols


def transform_bin2str(nonogram, nonogram_ones, nonogram_zeros):
    # TODO: Build an integer representation of the nonogram array to pass
    #       the test cases.
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


if __name__ == '__main__':
    clues = (((1,), (3,), (1,), (3, 1), (3, 1)),
             ((3,), (2,), (2, 2), (1,), (1, 2)),)
    ans = ((0, 0, 1, 1, 1),
           (0, 0, 0, 1, 1),
           (1, 1, 0, 1, 1),
           (0, 1, 0, 0, 0),
           (0, 1, 0, 1, 1))
    sol = Nonogram(clues).solve()
    print(sol)
