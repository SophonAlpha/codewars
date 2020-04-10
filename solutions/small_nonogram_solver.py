"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""

import functools
import itertools
import solutions.nonogram_solver_show as nshow


class NonogramCheckError(Exception):
    """
    Custom error class: thrown when the '1s' set in the nonogram don't match the
    row clues or column clues.
    """


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
        # set get all variants of filled squares based on the clues
        row_variants = get_all_variants(self.row_clues, self.nonogram_row_masks)
        for idx, nono_variant in enumerate(itertools.product(*row_variants)):
            if self.check(nono_variant):
                # Found a valid nonogram! Exit search loop.
                break
        print()
        return bin2tuple(nono_variant, self.num_cols)

    def show(self):
        reordered_col_clues = reorder(self.col_clues)
        nshow.show(self.nonogram_ones, self.nonogram_zeros,
                   reordered_col_clues, self.row_clues)

    def check(self, nono_variant):
        # check column '1s' match column clues
        length = self.num_rows
        col_clues = tuple(
            (tuple(clue.count('1')
                   for clue in f'{col:0{length}b}'.split('0') if clue)
             for col in cols2rows(nono_variant, self.num_cols))
        )
        col_clues = tuple(clue if clue else (0,) for clue in col_clues)
        return col_clues == self.col_clues


def reorder(items):
    return tuple(tuple(item[::-1]) for item in items)


def get_all_variants(clues, pos_masks):
    max_len = len(clues)
    items = [0, ] * max_len
    for idx, clue, mask in [(idx, clue, pos_masks[idx])
                            for idx, clue in enumerate(clues)]:
        if mask != 0:
            items[idx] = combinations(clue, mask, max_len)
    return items


def combinations(clue, mask, max_len):
    variants = []
    max_r_shift = max_len - (sum(clue) + len(clue) - 1)
    clue_shftd = init_shift(clue, max_len)
    for combination in combinator(clue_shftd, 0, 0, max_r_shift):
        variants.append(or_merge(combination[:]))
    return variants


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


def cols2rows(items, max_len):
    new_rows = []
    for idx in reversed(range(max_len)):
        new_rows.append(sum([((item & (1 << idx)) >> idx) << pos
                             for pos, item in enumerate(items)]))
    return new_rows


def bin2tuple(nonogram_ones, num_cols):
    fmt = '{0:0' + str(num_cols) + 'b}'
    nonogram = tuple(
        tuple(int(cell) for cell in fmt.format(item)) for item in nonogram_ones
    )
    return nonogram


if __name__ == '__main__':
    start_clues = (
        ((2, 1), (1,), (1, 1, 1), (1, 1), (3,), (2, 2), (4, 1)),
        ((1, 2, 1), (1, 2), (1, 1), (1, 1, 1), (1, 3), (3,), (1, 1))
    )
    ans = ((1, 0, 1, 1, 0, 1, 0),
           (1, 0, 0, 0, 0, 1, 1),
           (0, 0, 1, 0, 0, 0, 1),
           (1, 0, 0, 0, 1, 0, 1),
           (0, 0, 1, 0, 1, 1, 1),
           (0, 0, 0, 1, 1, 1, 0),
           (0, 1, 0, 0, 0, 0, 1))
    sol = Nonogram(start_clues).solve()
    print(sol)
