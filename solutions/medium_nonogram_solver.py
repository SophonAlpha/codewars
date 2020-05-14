"""
Solution for Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/

Performance optimization:

     9 May 2020, iterator through all variants of row clues: 29.338 seconds
    10 May 2020, iterate through row or columns dependent
                 on which one has the lowest number of
                 variants:                                    0.6501498 seconds
    14 May 2020, set common positions before iterating
                 through variants:                            0.1204889 seconds
                 don't process variants that don't match
                 already set positions:                       0.0655467 seconds

"""

import functools
import itertools
import solutions.nonogram_solver_show as nshow
import operator
import re
import pprint


def wrapper(func, *args, **kwargs):
    """
    Wrapper function for initialising generator functions.
    """

    def wrapped():
        return func(*args, **kwargs)

    return wrapped


class Nonogram:

    def __init__(self, clues):
        # check which way is faster column wise or row wise
        col_clues, row_clues = clues[0], clues[1]
        row_variants = functools.reduce(
            lambda x, y: x * y, num_variants(row_clues, len(col_clues)))
        col_variants = functools.reduce(
            lambda x, y: x * y, num_variants(col_clues, len(row_clues)))
        if row_variants <= col_variants:
            # process row wise
            self.swap = False
            self.col_clues, self.row_clues = reorder(col_clues), row_clues
        else:
            # process column wise
            self.swap = True
            self.col_clues, self.row_clues = reorder(row_clues), col_clues
        # initialise the nonogram
        self.nonogram_ones = [0, ] * len(self.row_clues)
        self.nonogram_zeros = [0, ] * len(self.row_clues)
        self.num_cols = len(self.col_clues)
        self.num_rows = len(self.row_clues)
        self.col_bit_mask = 2 ** self.num_cols - 1
        self.row_bit_mask = 2 ** self.num_rows - 1
        self.nonogram_col_masks = [self.col_bit_mask, ] * self.num_cols
        self.nonogram_masks = [self.row_bit_mask, ] * self.num_rows
        self.backups = []

    def solve(self):
        # set common positions in columns and rows
        self.set_common_positions()
        # solve the nonogram
        self.build(0, self.row_clues, self.num_cols)
        if self.swap:
            # turn the nonogram back
            self.nonogram_ones = transpose(self.nonogram_ones, self.num_cols)
            self.num_rows, self.num_cols = self.num_cols, self.num_rows
        return bin2tuple(self.nonogram_ones, self.num_cols)

    def build(self, idx, clues, max_len):
        clue = clues[idx]
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        clue_shftd = init_shift(clue, max_len)
        for combination in combinator(clue_shftd, 0, 0, max_r_shift):
            if self.nonogram_ones[idx] & combination != self.nonogram_ones[idx]:
                # the combination doesn't match the fields already set
                continue
            self.backup()
            self.nonogram_ones[idx] = combination
            self.set_zeros()
            self.update_nonogram_mask()
            if not self.nonogram_valid():
                variant_is_valid = False
                self.restore()
                self.update_nonogram_mask()
            else:
                variant_is_valid = True
                if idx + 1 < len(clues):
                    if self.build(idx + 1, clues, max_len):
                        break
                    else:
                        variant_is_valid = False
                        self.restore()
                        self.update_nonogram_mask()
                else:
                    break
        return variant_is_valid

    def set_common_positions(self):
        # set common positions in columns
        cols = find_common_positions(self.col_clues,
                                     self.nonogram_col_masks,
                                     self.num_rows)
        cols = rows2cols(cols, len(cols))
        self.set_ones(cols)
        self.set_zeros()
        self.update_nonogram_mask()
        # set common positions in rows
        rows = find_common_positions(self.row_clues,
                                     self.nonogram_masks,
                                     self.num_cols)
        self.set_ones(rows)
        self.set_zeros()
        self.update_nonogram_mask()

    def backup(self):
        self.backups.append(
            (self.nonogram_ones.copy(), self.nonogram_zeros.copy())
        )

    def restore(self):
        (self.nonogram_ones, self.nonogram_zeros) = self.backups.pop()

    def update_nonogram_mask(self):
        """
        In the nonogram mask a '1' indicates where a '1' can be placed. A row or
        column with all positions set to '0' indicates a solved row or column.

        The nonogram mask is maintained row-wise and column-wise.

        A nonogram is solved when all positions in the nonogram mask are set
        to '0'.
        """
        # combine ones & zeros with 'bitwise or' with the invert of the mask
        ones_zeros = [
            self.nonogram_ones[idx] ^ self.nonogram_zeros[idx]
            ^ self.col_bit_mask for idx, _ in enumerate(self.nonogram_ones)
        ]
        self.nonogram_masks = ones_zeros[:]

    def set_ones(self, items):
        self.nonogram_ones = [self.nonogram_ones[idx] | item
                              for idx, item in enumerate(items)]

    def set_zeros(self):
        # TODO: performance optimization. Skip rows and columns that are
        #       already complete.
        # TODO: performance optimization. Test if the correct number of clues
        #       is set at the beginning and end of the line. If yes, set the
        #       surrounding zeros.
        # set zeros in columns
        ones = cols2rows(self.nonogram_ones, self.num_cols)
        col_masks = cols2rows(self.nonogram_masks, self.num_cols)
        width = self.num_rows
        new_col_zeros = set_new_zeros(ones, col_masks, width, self.col_clues)
        new_col_zeros = rows2cols(new_col_zeros, self.num_rows)
        # set zeros in rows
        new_row_zeros = set_new_zeros(self.nonogram_ones,
                                      self.nonogram_masks,
                                      self.num_cols,
                                      self.row_clues)
        # combine new columns and rows zeros
        new_zeros = [row | new_col_zeros[idx]
                     for idx, row in enumerate(new_row_zeros)]
        # set zeros in nonogram
        self.nonogram_zeros = [row | new_zeros[idx]
                               for idx, row in enumerate(self.nonogram_zeros)]

    def show(self):
        reordered_col_clues = reorder(self.col_clues)
        nshow.show(self.nonogram_ones, self.nonogram_zeros,
                   reordered_col_clues, self.row_clues)

    def nonogram_valid(self):
        # TODO: refactor to reduce duplication of code for rows and columns
        # check that there is no overlap between the "ones" map and the "zeros"
        # map. If there is, this indicates that a choosen variant has
        # overwritten an already found "zero".
        # TODO: add test for mismatch at the beginning or end of row or column.
        #       e.g. (2,1) 10.....
        separate = [
            row ^ self.nonogram_zeros[idx] == row | self.nonogram_zeros[idx]
            for idx, row in enumerate(self.nonogram_ones)
        ]
        if not all(separate):
            return False
        # check row '1s' match row clues
        length = self.num_cols
        row_clues = tuple((tuple(clue.count('1')
                                 for clue in f'{row:0{length}b}'.split('0')
                                 if clue)
                           for row in self.nonogram_ones))
        row_clues = tuple(clue if clue else (0,) for clue in row_clues)
        rows_ok = [(self.nonogram_masks[idx] == 0 and
                    item == self.row_clues[idx]) or
                   (self.nonogram_masks[idx] != 0 and
                    sum(item) <= sum(self.row_clues[idx]))
                   for idx, item in enumerate(row_clues)]
        if not all(rows_ok):
            return False
        # check column '1s' match column clues
        length = self.num_rows
        col_masks = cols2rows(self.nonogram_masks, self.num_cols)
        col_clues = tuple((tuple(clue.count('1')
                                 for clue in f'{col:0{length}b}'.split('0')
                                 if clue)
                           for col in cols2rows(self.nonogram_ones,
                                                self.num_cols)))
        col_clues = tuple(clue if clue else (0,) for clue in col_clues)
        cols_ok = [(col_masks[idx] == 0 and
                    item == self.col_clues[idx]) or
                   (col_masks[idx] != 0 and
                    sum(item) <= sum(self.col_clues[idx]))
                   for idx, item in enumerate(col_clues)]
        if not all(cols_ok):
            return False
        return True


def num_variants(clues, length):
    total_variants = []
    for clue in clues:
        max_r_shift = length - (sum(clue) + len(clue) - 1)
        count = max_r_shift + 1
        if len(clue) > 1:
            count += sum(variants(max_r_shift, 1, len(clue) - 1))
        total_variants.append(count)
    return total_variants


def variants(max_r_shift, level, max_level):
    yield int(sum_arithmetic_seq(num=max_r_shift))
    if not (level + 1 > max_level):
        for num in range(max_r_shift, 0, -1):
            yield from variants(num, level + 1, max_level)


def sum_arithmetic_seq(first=1, diff=1, num=1):
    return (num / 2) * (2 * first + (num - 1) * diff)


def reorder(items):
    return tuple(tuple(item[::-1]) for item in items)


def find_common_positions(clues, pos_masks, max_len):
    """
    For all clues find the common positions. Common positions are fields in the
    nonogram that are always set no matter what variant of the clue is
    applied. For example: clue 3 in a 5 column nonogram row. There a three
    possible variants:
              v
    column: 01234
    1.)     11100
    2.)     01110
    3.)     00111

    Position (column) 2 is common in all variants of the clue. This common
    position can safely be set to '1'.
    """
    items = [0, ] * len(clues)
    for idx, clue, mask in [(idx, clue, pos_masks[idx])
                            for idx, clue in enumerate(clues)]:
        if mask != 0:
            max_r_shift = max_len - (sum(clue) + len(clue) - 1)
            shift = max_len
            cmn_positions = 0
            for elem in clue:
                shift = shift - elem
                if elem > max_r_shift:
                    overlap = elem - max_r_shift
                    cmn_positions |= (get_bits(overlap) << shift)
                shift = shift - 1
            items[idx] = cmn_positions
    return items


def get_bits(num):
    bits = 0
    for pos in range(num):
        bits = bits | 1 << pos
    return bits


def find_fixed_positions(clues, pos_masks, nonogram_ones):
    max_len = len(clues)
    items = [0, ] * max_len
    for idx, clue, mask in [(idx, clue, pos_masks[idx])
                            for idx, clue in enumerate(clues)]:
        if mask != 0 and nonogram_ones[idx] != 0:
            items[idx] = fixed_positions(clue, mask, max_len,
                                         nonogram_ones[idx])
    return items


def fixed_positions(clue, mask, max_len, nonogram_ones_line):
    option = 0
    max_r_shift = max_len - (sum(clue) + len(clue) - 1)
    clue_shftd = init_shift(clue, max_len)
    for combination in combinator(clue_shftd, 0, 0, max_r_shift):
        if (combination & (nonogram_ones_line | mask) == combination) and \
                (combination & nonogram_ones_line == nonogram_ones_line):
            if not option:
                option = combination
            else:
                option = 0
                break
    return option


def combinator(clue, idx, start_r_shift, max_r_shift):
    clue_shftd = clue[:]
    for r_shift in range(start_r_shift, max_r_shift + 1):
        clue_shftd[idx] = clue[idx] >> r_shift
        if idx < (len(clue) - 1):
            yield from combinator(clue_shftd, idx + 1, r_shift, max_r_shift)
        else:
            yield or_merge(clue_shftd)


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


def rows2cols(items, max_len):
    new_cols = []
    for idx, _ in enumerate(items):
        new_cols.append(sum([((item & (1 << idx)) >> idx) << (max_len - pos - 1)
                             for pos, item in enumerate(items)]))
    return new_cols


def transpose(items, max_len):
    new_rows = []
    for col_idx in reversed(range(max_len)):
        new_rows.append(sum(
            [((item & (1 << col_idx)) >> col_idx) << (max_len - row_idx - 1)
             for row_idx, item in enumerate(items)])
        )
    return new_rows


def set_new_zeros(ones, masks, width, clues):
    """
    Set the zeros for a nonogram array. The algorithm looks for the segments of
    '1s' and compares against the given clues. Where the number of '1s' matches
    the clue set the positions left and right to the '1s' to '0'.
    """
    new_zeros = [0] * len(ones)
    for idx, line in enumerate(ones):
        if masks[idx] == 0:
            continue
        segments = tuple(item.count('1')
                         for item in f'{line:0{width}b}'.split('0')
                         if item)
        # Check if reminder of line can be set to zero.
        if sum(segments) == sum(clues[idx]):
            # All clues found! Mark all remaining positions as zeros.
            new_zeros[idx] = (2 ** width - 1) ^ line
    return new_zeros


def find_neighbour_zeros(line, segments, clue, width):
    bits_to_set = 0
    segments_start_end = [(m.start(), m.end())
                          for m in re.finditer('1+', f'{line:0{width}b}')]
    for count_idx, count in enumerate(segments):
        if count == clue[count_idx]:
            start, end = segments_start_end[count_idx]
            if start > 0:
                bits_to_set = bits_to_set | 1 << (width - 1) - (start - 1)
            if end <= (width - 1):
                bits_to_set = bits_to_set | 1 << (width - 1) - end
    new_zeros = bits_to_set
    return new_zeros


def bin2tuple(nonogram_ones, num_cols):
    fmt = '{0:0' + str(num_cols) + 'b}'
    nonogram = tuple(
        tuple(int(cell) for cell in fmt.format(item)) for item in nonogram_ones
    )
    return nonogram


if __name__ == '__main__':
    clues = (((1, 1, 1), (2, 2), (3, 2), (3, 1),
              (1, 2), (1, 1, 2), (1, 1, 1), (3, 1)),
             ((1, 1, 2), (1, 1), (6,), (1, 1),
              (3, 2), (2, 1, 1), (1, 2), (1, 3))),
    ans = ((1, 0, 0, 1, 0, 1, 1, 0),
           (0, 1, 0, 1, 0, 0, 0, 0),
           (1, 1, 1, 1, 1, 1, 0, 0),
           (0, 0, 1, 0, 0, 0, 0, 1),
           (0, 1, 1, 1, 0, 0, 1, 1),
           (1, 1, 0, 0, 1, 0, 0, 1),
           (0, 0, 1, 0, 1, 1, 0, 0),
           (0, 0, 1, 0, 0, 1, 1, 1)),
    asymmetric_clues = (((1,), (2,), (4,), (1,), (1,), (5,), (2,), (1, 1)),
                        ((1, 1), (1, 2, 1), (3, 1), (2, 3), (1, 2)))
    asymmetric_ans = ((1, 0, 0, 0, 0, 1, 0, 0),
                      (0, 0, 1, 0, 1, 1, 0, 1),
                      (0, 1, 1, 1, 0, 1, 0, 0),
                      (0, 1, 1, 0, 0, 1, 1, 1),
                      (0, 0, 1, 0, 0, 1, 1, 0))
    nono = Nonogram(clues)
    sol = nono.solve()
    print()
    pprint.pprint(sol)
