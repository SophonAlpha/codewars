"""
Solution for Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

Try nonograms here: https://www.puzzle-nonograms.com/

Performance optimization:

     9 May 2020, iterator through all variants of row clues: 29.338 seconds
    10 May 2020, iterate through row or columns dependent
                 on which one has the lowest number of
                 variants:                                    0.6501498 seconds
    14 May 2020, set common positions before iterating
                 through variants:                            0.1204889 seconds
                 don't process variants that don't match
                 already set positions:                       0.0655467 seconds
    19 May 2020, remove the need for a bit mask to detect
                 completion of the nonogram:                  0.0343510 seconds
    24 May 2020, replaced recursive approach with while loop,
                 process rows in order of number of variants,
                 lowest number of variants first:             0.0658589 seconds
                 100 tests (9x9) passed in                  177.74 seconds
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

    def __init__(self, row_clues, col_clues):
        self.num_rows = len(row_clues)
        self.num_cols = len(col_clues)

        self.row_num_bits = self.num_cols
        self.row_bit_mask = 2 ** self.num_cols - 1
        self.col_num_bits = self.num_rows
        self.col_bit_mask = 2 ** self.num_rows - 1

        self.row_ones = [0, ] * len(row_clues)
        self.row_zeros = [0, ] * len(row_clues)
        # TODO: Check if masks can be removed.
        self.row_masks = [self.row_bit_mask, ] * self.num_rows
        self.col_ones = [0, ] * len(col_clues)
        self.col_zeros = [0, ] * len(col_clues)
        # TODO: Check if masks can be removed.
        self.col_masks = [self.col_bit_mask, ] * self.num_cols

        self.backups = []

    def set_ones(self, rows=None, cols=None):
        if rows:
            self.row_ones, self.col_ones = self.__set_bits(
                rows,
                self.row_ones, self.row_num_bits,
                self.col_ones, self.col_num_bits,
                axis='rows')
        if cols:
            self.col_ones, self.row_ones = self.__set_bits(
                cols,
                self.row_ones, self.row_num_bits,
                self.col_ones, self.col_num_bits,
                axis='cols')

    def set_zeros(self, rows=None, cols=None):
        if rows:
            self.row_zeros, self.col_zeros = self.__set_bits(
                rows,
                self.row_zeros, self.row_num_bits,
                self.col_zeros, self.col_num_bits,
                axis='rows')
        if cols:
            self.col_zeros, self.row_zeros = self.__set_bits(
                cols,
                self.row_zeros, self.row_num_bits,
                self.col_zeros, self.col_num_bits,
                axis='cols')

    def __set_bits(self, items, row_ones, row_num_bits, col_ones, col_num_bits,
                   axis='rows'):
        if axis == 'rows':
            direction = 1
            first_ones = row_ones
            first_num_bits = row_num_bits
            second_ones = col_ones
            second_num_bits = col_num_bits
        elif axis == 'cols':
            direction = -1
            first_ones = col_ones
            first_num_bits = col_num_bits
            second_ones = row_ones
            second_num_bits = row_num_bits
        bit_shift = list(range(second_num_bits))[::direction]
        for idx, item in items:
            first_ones[idx] = first_ones[idx] | item
            second_ones = [
                second_ones[bit_idx] | (int(bit) << bit_shift[idx])
                for bit_idx, bit in
                enumerate(f'{item:0{first_num_bits}b}'[::direction])
            ]
        return first_ones, second_ones

    def complete(self):
        """
        Check if the nonogram has been completed. Completed means all fields are
        either set to "one" or "zero". Important: this function does not check
        if the completed nonogram is correct.
        """
        completed = [
            (self.row_ones[idx] ^ self.row_zeros[idx] ^ self.row_bit_mask) == 0
            for idx in range(self.num_rows)]
        return all(completed)

    def backup(self):
        """
        Save current state of the nonogram arrays in a FIFO stack.
        """
        self.backups.append(
            (self.row_ones.copy(),
             self.row_zeros.copy(),
             self.row_masks.copy(),
             self.col_ones.copy(),
             self.col_zeros.copy(),
             self.col_masks.copy())
        )

    def restore(self):
        """
        Restore nonogram arrays from FIFO stack.
        """
        (self.row_ones,
         self.row_zeros,
         self.row_masks,
         self.col_ones,
         self.col_zeros,
         self.col_masks) = self.backups.pop()


class Nonogram:

    def __init__(self, clues):
        # Check which way it is faster to process the clues. Column wise or
        # row wise?
        col_clues, row_clues = clues[0], clues[1]
        self.row_variants = sorted(num_variants(row_clues, len(col_clues)),
                                   key=lambda item: item[1])
        self.col_variants = sorted(num_variants(col_clues, len(row_clues)),
                                   key=lambda item: item[1])
        total_row_variants = functools.reduce(
            lambda x, y: x * y, [elem for _, elem in self.row_variants])
        total_col_variants = functools.reduce(
            lambda x, y: x * y, [elem for _, elem in self.col_variants])
        if total_row_variants <= total_col_variants:
            # process row wise
            self.swap = False
            self.col_clues, self.row_clues = reorder(col_clues), row_clues
        else:
            # process column wise
            self.swap = True
            self.col_clues, self.row_clues = reorder(row_clues), col_clues
            self.col_variants, self.row_variants = self.row_variants, \
                                                   self.col_variants
        # initialise the nonogram array
        self.nono = NonoArray(self.row_clues, self.col_clues)

    def solve(self):
        self.build(0, self.row_clues, self.nono.num_cols)
        if self.swap:
            # turn the nonogram back
            self.nono.row_ones = transpose(
                self.nono.row_ones, self.nono.num_cols)
            self.nono.num_rows, self.nono.num_cols = self.nono.num_cols, \
                                                     self.nono.num_rows
        return bin2tuple(self.nono.row_ones, self.nono.num_cols)

    def build(self, idx, clues, max_len):
        # set common positions in columns and rows
        self.set_common_positions()
        self.deduct_zeros()
        # solve the nonogram
        varis = {}
        idx = self.choose_row()
        varis[idx] = combinations(self.nono, idx, clues, max_len)
        while not self.nono.complete():
            try:
                variant = next(varis[idx])
            except StopIteration:
                self.nono.restore()
                idx = self.choose_row()
                continue
            if (((self.nono.row_ones[idx] | self.nono.row_zeros[idx]) ^
                  self.nono.row_bit_mask) | self.nono.row_ones[idx]) & \
                  variant != variant:
                # the variant doesn't match the fields already set
                continue
            self.nono.backup()
            self.nono.set_ones(rows=[(idx, variant)])
            self.nono.set_zeros(
                rows=[(idx, variant ^ self.nono.row_bit_mask)])
            self.deduct_zeros()
            self.deduct_gaps_for_ones()
            self.deduct_missing_ones()
            if not self.nonogram_valid():
                self.nono.restore()
            else:
                idx = self.choose_row()
                varis[idx] = combinations(self.nono, idx, clues, max_len)

    def choose_row(self):
        row = None
        for idx, num in self.row_variants:
            if (self.nono.row_ones[idx] ^
                self.nono.row_zeros[idx] ^
                self.nono.row_bit_mask) != 0:
                row = idx
                break
        return row

    def set_common_positions(self):
        # set common positions in columns
        cols = deduct_common_positions(self.col_clues, self.nono.num_rows)
        self.nono.set_ones(cols=cols)
        # set common positions in rows
        rows = deduct_common_positions(self.row_clues, self.nono.num_cols)
        self.nono.set_ones(rows=rows)

    def deduct_zeros(self):
        # TODO: performance optimization. Test if the correct number of clues
        #       is set at the beginning and end of the line. If yes, set the
        #       surrounding zeros.
        col_zeros = set_new_zeros(self.nono.col_ones,
                                  self.nono.col_zeros,
                                  self.nono.col_num_bits,
                                  self.nono.col_bit_mask,
                                  self.col_clues)
        self.nono.set_zeros(cols=col_zeros)
        row_zeros = set_new_zeros(self.nono.row_ones,
                                  self.nono.row_zeros,
                                  self.nono.row_num_bits,
                                  self.nono.row_bit_mask,
                                  self.row_clues)
        self.nono.set_zeros(rows=row_zeros)

    def deduct_gaps_for_ones(self):
        rows = fill_gaps(self.nono.row_ones,
                         self.nono.row_zeros,
                         self.nono.row_bit_mask,
                         self.nono.row_num_bits,
                         self.row_clues)
        self.nono.set_ones(rows=rows)
        cols = fill_gaps(self.nono.col_ones,
                         self.nono.col_zeros,
                         self.nono.col_bit_mask,
                         self.nono.col_num_bits,
                         self.col_clues)
        self.nono.set_ones(cols=cols)

    def show(self):
        """
        Helper function to visualize the nonogram.
        """
        reordered_col_clues = reorder(self.col_clues)
        nshow.show(self.nono.row_ones, self.nono.row_zeros,
                   reordered_col_clues, self.row_clues)

    def nonogram_valid(self):
        # TODO: add test for mismatch at the beginning or end of row or column.
        #       e.g. (2,1) 10.....
        # TODO: check for this scenario:
        #            1,3 |   |   |   | 0 |   | 0 |   | 0 |
        #                there is no space left for 3 consecutive 1's
        # TODO: check for this scenario:
        #          2,1,1 |   |   | 0 | 1 | 0 | 1 |   | 1 |
        #                three clues set but they don't match the give clues
        # Check that "ones" and "zeros" are separate and don't overlap. Overlap
        # would be when a position is marked with "one" in nonogram_ones and
        # nonogram_zeros. If there is, this indicates that a chosen variant has
        # overwritten an already found "zero". Therefore the variant is invalid.
        if not is_separate(self.nono.row_ones, self.nono.row_zeros):
            return False
        # Check column '1s' match column clues.
        if not clues_correct(self.nono.col_ones,
                             self.nono.col_zeros,
                             self.nono.col_masks,
                             self.nono.col_num_bits,
                             self.nono.col_bit_mask,
                             self.col_clues):
            return False
        # Please note: It is not required to check the row clues for
        # correctness. Rows are generated in a way that they are always correct.
        return True


def is_separate(nonogram_ones, nonogram_zeros):
    separate = [
        row ^ nonogram_zeros[idx] == row | nonogram_zeros[idx]
        for idx, row in enumerate(nonogram_ones)
    ]
    return all(separate)


def clues_correct(ones, zeros, masks, num_bits, all_bits_mask, clues):
    # Transform integer representation of the nonogram into string
    # representation.
    indexes = []
    ones_str = []
    for idx, item in enumerate(ones):
        ones_str.append(f'{item:0{num_bits}b}'.replace('0', ' '))
        if (ones[idx] ^ zeros[idx] ^ all_bits_mask) != 0:
            indexes.append(idx)
    zeros_str = [f'{item:0{num_bits}b}'.replace('0', ' ') for item in zeros]
    for idx_one, one in enumerate(ones_str):
        for idx_zero, char in enumerate(zeros_str[idx_one]):
            if char == '1':
                ones_str[idx_one] = ones_str[idx_one][:idx_zero] + '0' + \
                                    ones_str[idx_one][idx_zero + 1:]
    # Check whether clues fit in remaining gaps between '0's.
    gaps = [[m.end() - m.start() for m in re.finditer(' +', item)]
            for item in zeros_str]
    clues_cp = [list(item) for item in clues]
    for idx in indexes:
        while clues_cp[idx] and gaps[idx]:
            if clues_cp[idx][-1] < gaps[idx][-1]:
                gaps[idx][-1] = gaps[idx][-1] - clues_cp[idx][-1] - 1
                clues_cp[idx].pop(-1)
            elif clues_cp[idx][-1] == gaps[idx][-1]:
                gaps[idx].pop(-1)
                clues_cp[idx].pop(-1)
            else:
                gaps[idx].pop(-1)
        if clues_cp[idx]:
            # There are clues left. Means not all clues fit in the gaps.
            return False
    # Get the start and end positions of all segments of '1's.
    check_clues = list()
    for item in ones_str:
        check_clues.append(
            tuple(
                m.end() - m.start()
                for m in re.finditer('(?<=^)1+(?=0|$)|(?<=0)1+(?=0|$)', item)
                if (m.end() - m.start()) > 0
            ))
    # Check if the segments of '1's violate the given clues.
    check_clues = [((ones[idx] ^ zeros[idx] ^ all_bits_mask) == 0 and
                    item == clues[idx]) or
                   ((ones[idx] ^ zeros[idx] ^ all_bits_mask) != 0 and
                    len(item) <= len(clues[idx]) and
                    sum(item) <= sum(clues[idx])) or
                   (len(item) == len(clues[idx]) and
                    item == clues[idx])
                   for idx, item in enumerate(check_clues)]
    return all(check_clues)


def num_variants(clues, max_bit_length):
    total_variants = []
    for idx, clue in enumerate(clues):
        max_r_shift = max_bit_length - (sum(clue) + len(clue) - 1)
        count = max_r_shift + 1
        if len(clue) > 1:
            count += sum(variants(max_r_shift, 1, len(clue) - 1))
        total_variants.append((idx, count))
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


def deduct_common_positions(clues, max_len):
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
    items = []
    for idx, clue in [(idx, clue)
                      for idx, clue in enumerate(clues)]:
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        shift = max_len
        cmn_positions = 0
        for elem in clue:
            shift = shift - elem
            if elem > max_r_shift:
                overlap = elem - max_r_shift
                cmn_positions |= (get_bits(overlap) << shift)
            shift = shift - 1
        items.append((idx, cmn_positions))
    return items


def get_bits(num):
    bits = 0
    for pos in range(num):
        bits = bits | 1 << pos
    return bits


# TODO: catch this case: 2,2 |   |   |   | 1 |   | 1 |   | 0 |
#                                                      ^
#                                                must be 1
# TODO: catch this case: 1,3 |   |   |   | 0 |   | 0 |   | 0 |
#                        invalid nonogram, 3 doesn't fit anywhere
def fill_gaps(ones, zeros, bit_mask, num_bits, clues):
    """
    Fill the gaps that match exactly the clues.
    """
    items = []
    for idx, elem in enumerate(zeros):
        if (ones[idx] ^ zeros[idx] ^ bit_mask) == 0:
            # skip lines already completed
            continue
        # Get length, start and end positions of gaps.
        gaps = [
            (m.end() - m.start(), m.start(), m.end())
            for m in re.finditer('0+', f'{elem:0{num_bits}b}')
        ]
        # Get the gaps that can be filled with '1's.
        fill_with_ones = list()
        clues_cp = list(clues[idx])
        while gaps and clues_cp:
            if gaps[-1][0] == clues_cp[-1]:  # right side
                fill_with_ones.append((gaps[-1][1], gaps[-1][2]))
            if gaps[0][0] == clues[0]:  # left side
                fill_with_ones.append((gaps[0][1], gaps[0][2]))
            gaps.pop(-1)
            clues_cp.pop(-1)
            gaps.pop(0) if gaps else False
            clues_cp.pop(0) if clues_cp else False
        # Fill the gaps with '1's.
        if not fill_with_ones:
            continue
        new_ones = '0' * num_bits
        for start, end in fill_with_ones:
            new_ones = new_ones[:start] + '1' * (end - start) + new_ones[end:]
        new_ones = int(new_ones, 2)
        items.append((idx, new_ones))
    return items


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


def combinations(nono, idx, clues, max_len):
    clue = clues[idx]
    max_r_shift = max_len - (sum(clue) + len(clue) - 1)
    clue_shftd = init_shift(clue, max_len)
    yield from combinator(nono, clue_shftd, 0, 0, max_r_shift, max_len)


def combinator(nono, clue, idx, start_r_shift, max_r_shift, max_len):
    clue_shftd = clue[:]
    for r_shift in range(start_r_shift, max_r_shift + 1):
        clue_shftd[idx] = clue[idx] >> r_shift
        if idx < (len(clue) - 1):
            yield from combinator(nono, clue_shftd, idx + 1,
                                  r_shift, max_r_shift, max_len)
        else:
            merged_clue_shftd = or_merge(clue_shftd)
            yield merged_clue_shftd


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


def set_new_zeros(ones, zeros, num_bits, bit_mask, clues):
    """
    Set the zeros for a nonogram array. The algorithm looks for the segments of
    '1s' and compares against the given clues. If matches set all remaining
    positions to '0'.
    """
    new_zeros = []
    for idx, line in enumerate(ones):
        if (ones[idx] ^ zeros[idx] ^ bit_mask) == 0:
            # skip lines already completed
            continue
        segments = tuple(item.count('1')
                         for item in f'{line:0{num_bits}b}'.split('0')
                         if item)
        if sum(segments) == sum(clues[idx]): # TODO: check if we can do segments == clues[idx]
            # All clues found! Mark all remaining positions as zeros.
            # new_zeros[idx] = all_bits_mask ^ line
            new_zeros.append((idx, bit_mask ^ line))
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
    nonogram = Nonogram(test_clues)
    sol = nonogram.solve()
    print()
    pprint.pprint(sol)
