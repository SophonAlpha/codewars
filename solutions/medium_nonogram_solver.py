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


class NonoArray:

    def __init__(self, clues):
        self.num_rows = 0
        self.num_cols = 0
        self.row_ones = []
        self.row_zeros = []
        self.row_masks = []
        self.col_ones = []
        self.col_zeros = []
        self.col_masks = []

    def set_ones(self):
        pass

    def set_zeros(self):
        pass

    def update_mask(self):
        pass

    def backup(self):
        pass

    def restore(self):
        pass


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
        self.num_cols = len(self.col_clues)
        self.row_num_bits = self.num_cols
        self.row_bit_mask = 2 ** self.num_cols - 1
        self.num_rows = len(self.row_clues)
        self.col_num_bits = self.num_rows
        self.col_bit_mask = 2 ** self.num_rows - 1
        self.nono_row_ones = [0, ] * len(self.row_clues)
        self.nono_row_zeros = [0, ] * len(self.row_clues)
        self.nono_row_masks = [self.row_bit_mask, ] * self.num_rows
        self.nono_col_ones = [0, ] * len(self.col_clues)
        self.nono_col_zeros = [0, ] * len(self.col_clues)
        self.nono_col_masks = [self.col_bit_mask, ] * self.num_cols
        self.backups = []

    def solve(self):
        # set common positions in columns and rows
        self.set_common_positions()
        self.set_zeros()

        # self.update_nonogram_mask()

        # solve the nonogram
        self.build(0, self.row_clues, self.num_cols)
        if self.swap:
            # turn the nonogram back
            self.nono_row_ones = transpose(self.nono_row_ones, self.num_cols)
            self.num_rows, self.num_cols = self.num_cols, self.num_rows
        return bin2tuple(self.nono_row_ones, self.num_cols)

    def build(self, idx, clues, max_len):
        variant_is_valid = False
        clue = clues[idx]
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        clue_shftd = init_shift(clue, max_len)
        for combination, col_bits in combinator(clue_shftd, 0, 0,
                                                max_r_shift, max_len):
            if self.nono_row_ones[idx] & combination != self.nono_row_ones[idx]:
                # the combination doesn't match the fields already set
                continue
            self.backup()
            self.nono_row_ones[idx] = combination
            self.nono_row_zeros[idx] = combination ^ self.row_bit_mask
            bit_filter = self.col_bit_mask ^ (1 << idx)
            self.nono_col_ones = [
                (self.nono_col_ones[col_idx] & bit_filter) | (bit << idx)
                for col_idx, bit in enumerate(col_bits)
            ]
            self.nono_col_zeros = [
                (self.nono_col_zeros[col_idx] & bit_filter) | ((bit ^ 1) << idx)
                for col_idx, bit in enumerate(col_bits)
            ]
            self.set_zeros()
            # self.update_nonogram_mask()
            if not self.nonogram_valid():
                variant_is_valid = False
                self.restore()
                # self.update_nonogram_mask()
            else:
                variant_is_valid = True
                if idx + 1 < len(clues):
                    if self.build(idx + 1, clues, max_len):
                        break
                    else:
                        variant_is_valid = False
                        self.restore()
                        # self.update_nonogram_mask()
                else:
                    break
        return variant_is_valid

    def set_common_positions(self):
        # set common positions in columns
        cols = find_common_positions(self.col_clues,
                                     self.nono_col_masks,
                                     self.num_rows)
        self.nono_col_ones = [self.nono_col_ones[col_idx] | col
                              for col_idx, col in enumerate(cols)]
        cols = rows2cols(cols, len(cols))
        self.set_ones(cols)
        # set common positions in rows
        rows = find_common_positions(self.row_clues,
                                     self.nono_row_masks,
                                     self.num_cols)
        self.set_ones(rows)

    def backup(self):
        self.backups.append(
            (self.nono_row_ones.copy(),
             self.nono_row_zeros.copy(),
             self.nono_row_masks.copy(),
             self.nono_col_ones.copy(),
             self.nono_col_zeros.copy(),
             self.nono_col_masks.copy())
        )

    def restore(self):
        (self.nono_row_ones,
         self.nono_row_zeros,
         self.nono_row_masks,
         self.nono_col_ones,
         self.nono_col_zeros,
         self.nono_col_masks) = self.backups.pop()

    def update_nonogram_mask(self):
        """
        In the nonogram mask a '1' indicates an undecided position (can be
        either a one or a zero). A row or column with all positions set to '0'
        indicates a completed row or column.

        The nonogram mask is maintained row-wise and column-wise.

        A nonogram is solved when all positions in the nonogram mask are set
        to '0'.
        """

        # combine ones & zeros with 'bitwise or' with the invert of the mask
        self.nono_row_masks = [
            self.nono_row_ones[idx] ^ self.nono_row_zeros[idx]
            ^ self.col_bit_mask for idx, _ in enumerate(self.nono_row_ones)
        ]

        check_nono_col_masks = [
            self.nono_col_ones[idx] ^ self.nono_col_zeros[idx]
            ^ self.row_bit_mask for idx, _ in enumerate(self.nono_col_ones)
        ]

        row_masks_txt = [f'{row_mask:0{self.num_cols}b}'
                         for row_mask in self.nono_row_masks]
        self.nono_col_masks = [
            or_merge(
                [int(row_mask[col_idx]) << row_idx
                 for row_idx, row_mask in enumerate(row_masks_txt)]
            )
            for col_idx in range(self.num_cols)
        ]

        if check_nono_col_masks != self.nono_col_masks:
            print('Masks don\'t match')

    def set_ones(self, items):
        self.nono_row_ones = [self.nono_row_ones[idx] | item
                              for idx, item in enumerate(items)]
        row_ones_txt = [f'{row:0{self.row_num_bits}b}'
                         for row in self.nono_row_ones]
        self.nono_col_ones = [
            or_merge(
                [int(row[col_idx]) << row_idx
                 for row_idx, row in enumerate(row_ones_txt)]
            )
            for col_idx, _ in enumerate(self.nono_col_ones)
        ]

    def set_zeros(self):
        # TODO: performance optimization. Skip rows and columns that are
        #       already complete.
        # TODO: performance optimization. Test if the correct number of clues
        #       is set at the beginning and end of the line. If yes, set the
        #       surrounding zeros.
        # set zeros in columns
        new_col_zeros = set_new_zeros(self.nono_col_ones,
                                      self.nono_col_zeros,
                                      self.nono_col_masks,
                                      self.col_num_bits,
                                      self.col_bit_mask,
                                      self.col_clues)
        new_col_zeros = rows2cols(new_col_zeros, self.num_rows)
        # set zeros in rows
        new_row_zeros = set_new_zeros(self.nono_row_ones,
                                      self.nono_row_zeros,
                                      self.nono_row_masks,
                                      self.row_num_bits,
                                      self.row_bit_mask,
                                      self.row_clues)
        # combine new columns and rows zeros
        new_zeros = [row | new_col_zeros[idx]
                     for idx, row in enumerate(new_row_zeros)]
        # set zeros in nonogram
        if sum(new_zeros) > 0:
            self.nono_row_zeros = [
                row | new_zeros[idx]
                for idx, row in enumerate(self.nono_row_zeros)
            ]
            row_zeros_txt = [f'{row:0{self.row_num_bits}b}'
                             for row in self.nono_row_zeros]
            self.nono_col_zeros = [
                or_merge(
                    [int(row[col_idx]) << row_idx
                     for row_idx, row in enumerate(row_zeros_txt)]
                )
                for col_idx, _ in enumerate(self.nono_col_zeros)
            ]

    def show(self):
        reordered_col_clues = reorder(self.col_clues)
        nshow.show(self.nono_row_ones, self.nono_row_zeros,
                   reordered_col_clues, self.row_clues)

    def nonogram_valid(self):
        # TODO: add test for mismatch at the beginning or end of row or column.
        #       e.g. (2,1) 10.....
        # Check that "ones" and "zeros" are separate and don't overlap. Overlap
        # would be when a position is marked with "one" in nonogram_ones and
        # nonogram_zeros. If there is, this indicates that a chosen variant has
        # overwritten an already found "zero". Therefore the variant is invalid.
        if not is_separate(self.nono_row_ones, self.nono_row_zeros):
            return False
        # check column '1s' match column clues
        if not clues_correct(self.nono_col_ones,
                             self.nono_col_zeros,
                             self.nono_col_masks,
                             self.col_num_bits,
                             self.col_bit_mask,
                             self.col_clues):
            return False
        return True


def is_separate(nonogram_ones, nonogram_zeros):
    separate = [
        row ^ nonogram_zeros[idx] == row | nonogram_zeros[idx]
        for idx, row in enumerate(nonogram_ones)
    ]
    return all(separate)


def clues_correct(ones, zeros, masks, num_bits, all_bits_mask, clues):
    check_clues = tuple((tuple(clue.count('1')
                               for clue in f'{row:0{num_bits}b}'.split('0')
                               if clue) for row in ones))
    check_clues = tuple(clue if clue else (0,) for clue in check_clues)

    # check_clues = [(masks[idx] == 0 and
    #                 item == clues[idx]) or
    #                (masks[idx] != 0 and
    #                 sum(item) <= sum(clues[idx]))
    #                for idx, item in enumerate(check_clues)]

    check_clues = [((ones[idx] ^ zeros[idx] ^ all_bits_mask) == 0 and
                    item == clues[idx]) or
                   ((ones[idx] ^ zeros[idx] ^ all_bits_mask) != 0 and
                    sum(item) <= sum(clues[idx]))
                   for idx, item in enumerate(check_clues)]

    return all(check_clues)


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
            # TODO: return tuples of (index, item) to reduce number of loops
            #       when applying changes to the nonogram.
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
    for combination in combinator(clue_shftd, 0, 0, max_r_shift, max_len):
        if (combination & (nonogram_ones_line | mask) == combination) and \
                (combination & nonogram_ones_line == nonogram_ones_line):
            if not option:
                option = combination
            else:
                option = 0
                break
    return option


def combinator(clue, idx, start_r_shift, max_r_shift, max_len):
    clue_shftd = clue[:]
    for r_shift in range(start_r_shift, max_r_shift + 1):
        clue_shftd[idx] = clue[idx] >> r_shift
        if idx < (len(clue) - 1):
            yield from combinator(clue_shftd, idx + 1,
                                  r_shift, max_r_shift, max_len)
        else:
            merged_clue_shftd = or_merge(clue_shftd)
            col_bits = [int(char)
                        for char in f'{merged_clue_shftd:0{max_len}b}']
            yield merged_clue_shftd, col_bits


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


def set_new_zeros(ones, zeros, masks, num_bits, all_bits_mask, clues):
    """
    Set the zeros for a nonogram array. The algorithm looks for the segments of
    '1s' and compares against the given clues. Where the number of '1s' matches
    the clue set the positions left and right to the '1s' to '0'.
    """
    new_zeros = [0] * len(ones)
    for idx, line in enumerate(ones):

        # if masks[idx] == 0:
        #     continue

        if (ones[idx] ^ zeros[idx] ^ all_bits_mask) == 0:
            continue

        segments = tuple(item.count('1')
                         for item in f'{line:0{num_bits}b}'.split('0')
                         if item)
        # Check if reminder of line can be set to zero.
        if sum(segments) == sum(clues[idx]):
            # All clues found! Mark all remaining positions as zeros.
            new_zeros[idx] = (2 ** num_bits - 1) ^ line
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
    test_clues = (((1, 1, 1), (2, 2), (3, 2), (3, 1),
                   (1, 2), (1, 1, 2), (1, 1, 1), (3, 1)),
                  ((1, 1, 2), (1, 1), (6,), (1, 1),
                   (3, 2), (2, 1, 1), (1, 2), (1, 3)))
    test_ans = ((1, 0, 0, 1, 0, 1, 1, 0),
                (0, 1, 0, 1, 0, 0, 0, 0),
                (1, 1, 1, 1, 1, 1, 0, 0),
                (0, 0, 1, 0, 0, 0, 0, 1),
                (0, 1, 1, 1, 0, 0, 1, 1),
                (1, 1, 0, 0, 1, 0, 0, 1),
                (0, 0, 1, 0, 1, 1, 0, 0),
                (0, 0, 1, 0, 0, 1, 1, 1))
    asymmetric_clues = (((1,), (2,), (4,), (1,), (1,), (5,), (2,), (1, 1)),
                        ((1, 1), (1, 2, 1), (3, 1), (2, 3), (1, 2)))
    asymmetric_ans = ((1, 0, 0, 0, 0, 1, 0, 0),
                      (0, 0, 1, 0, 1, 1, 0, 1),
                      (0, 1, 1, 1, 0, 1, 0, 0),
                      (0, 1, 1, 0, 0, 1, 1, 1),
                      (0, 0, 1, 0, 0, 1, 1, 0))
    nono = Nonogram(test_clues)
    sol = nono.solve()
    print()
    pprint.pprint(sol)
