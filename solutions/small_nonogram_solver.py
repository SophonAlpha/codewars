"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""

import functools
import solutions.small_nonogram_solver_show as nshow
from math import log


class Nonogram:

    def __init__(self, clues):
        self.col_clues, self.row_clues = reorder(clues[0]), clues[1]
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
            prev_ones = self.nonogram_ones[:]
            prev_zeros = self.nonogram_zeros[:]
            # set positions in columns
            col_pos_masks = self.get_col_masks()
            cols = common_positions(self.col_clues, col_pos_masks)
            cols = rows2cols(cols, len(cols))
            self.set_ones(cols)
            self.set_zeros()
            self.update_nonogram_mask()
            # set positions in rows
            row_pos_masks = self.get_row_masks()
            rows = common_positions(self.row_clues, row_pos_masks)
            self.set_ones(rows)
            self.set_zeros()
            self.update_nonogram_mask()
            # check if reach a state of no progress
            if not self.is_solved() and \
                    not progress(prev_ones, self.nonogram_ones,
                                 prev_zeros, self.nonogram_zeros):
                self.set_one_position()
                self.set_zeros()
                self.update_nonogram_mask()
        return bin2tuple(self.nonogram_ones, self.num_cols)

    def is_solved(self):
        return sum(self.nonogram_row_masks) + sum(self.nonogram_col_masks) == 0

    def update_nonogram_mask(self):
        # combine ones & zeros with bitwise or with the invert of the mask
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

    def set_one_position(self):
        # Find a row with a non-zero mask value. A mask value of zero for a row
        # means the row has been solved already. Any mask value > 0 indicates
        # a row with unsolved positions.
        idx = self.nonogram_row_masks.index(max(self.nonogram_row_masks))
        possible_bits = (self.nonogram_ones[idx] ^ self.nonogram_row_masks[idx])
        bit_to_set = 2**high_bit_order(possible_bits)
        self.nonogram_ones[idx] = self.nonogram_ones[idx] | bit_to_set

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
        reordered_col_clues = reorder(self.col_clues)
        nshow.show(self.nonogram_ones, self.nonogram_zeros,
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
    max_len = len(clues)
    items = [0, ] * max_len
    for idx, clue, mask in [(idx, clue, pos_masks[idx])
                            for idx, clue in enumerate(clues)]:
        if mask != 0:
            items[idx] = combinations(clue, mask, max_len)
    return items


def combinations(clue, mask, max_len):
    positions = None
    max_r_shift = max_len - (sum(clue) + len(clue) - 1)
    clue_shftd = init_shift(clue, max_len)
    for combination in combinator(clue_shftd, 0, 0, max_r_shift):
        combination = or_merge(combination)
        if (combination & mask == combination) and (positions is None):
            # store very first value
            positions = combination
        elif (combination & mask == combination) and positions:
            # bitwise 'and' with any subsequent value
            positions = and_merge([positions, combination])
        if positions == 0:
            break
    return positions


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


def bin2tuple(nonogram_ones, num_cols):
    fmt = '{0:0' + str(num_cols) + 'b}'
    nonogram = tuple(
        tuple(int(cell) for cell in fmt.format(item)) for item in nonogram_ones
    )
    return nonogram


def progress(prev_ones, nonogram_ones, prev_zeros, nonogram_zeros):
    return prev_ones != nonogram_ones or prev_zeros != nonogram_zeros


def high_bit_order(n):
    """
    Source: https://www.daniweb.com/programming/software-development/code/406590/lowest-highest-bit-set-in-integer

    Return the integer k >= 0 such that 2**k <= n < 2**(k+1).
    This is also the order of the last bit set in the bitwise representation of n.
    Raise value error if n <= 0
        * for n == 0, no bit is set.
        * for n < 0, an infinite number of bits are set.
    For example
        high_bit_order(2368) --> 11
        n = 2368  bits: 000000101001000000000000000...
        n = -2368 bits: 000000110110111111111111111...
        n = 2**11 bits: 000000000001000000000000000...
    This function checks its return value and raise ValueError if an error
    is detected.
    """
    k = int(log(n, 2))
    if k:
        x = n >> (k-1)
        if x == 1: # correct log() imprecision for very large integers
            return k - 1
        elif 2 <= x < 4:
            return k
        else: # very unlikely, but handled
            raise ValueError("high_bit_order() failed on unusual value.")
    else:
        return k


if __name__ == '__main__':
    start_clues = (((1,), (1, 1), (2,), (1, 2), (1, 1)),
                   ((1,), (1, 1), (1,), (4,), (2,)))
    ans = ((0, 0, 0, 0, 1),
           (0, 1, 0, 1, 0),
           (0, 0, 0, 0, 1),
           (1, 1, 1, 1, 0),
           (0, 0, 1, 1, 0))
    sol = Nonogram(start_clues).solve()
    print(sol)
