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
    9 June 2020, use regex to deduct positions for '0's
                 and '1's:                                    0.0193118 seconds
                 100 tests (9x9) passed in                    1.983 seconds
   17 June 2020, refinement for detecting patterns for
                 setting '1's (12x12_complex test case):     64.1435230 seconds
"""

import functools
import itertools
import solutions.nonogram_solver_show as nshow
import operator
import re
import pprint

GAPS_PATTERN = re.compile('[1 ]+')


def wrapper(func, *args, **kwargs):
    """
    Wrapper function for initialising generator functions.
    """

    def wrapped():
        return func(*args, **kwargs)

    return wrapped


class NonogramError(Exception):
    """
    Custom error class: thrown when an invalid nonogram has been detected.
    """


class NonoArray:

    def __init__(self, row_clues, col_clues):
        self.num_rows = len(row_clues)
        self.num_cols = len(col_clues)

        self.row_num_bits = self.num_cols
        self.row_bit_mask = 2 ** self.num_cols - 1
        self.col_num_bits = self.num_rows
        self.col_bit_mask = 2 ** self.num_rows - 1

        # TODO: refactor out integer representation of nonogram
        self.row_ones = [0, ] * len(row_clues)
        self.row_zeros = [0, ] * len(row_clues)
        self.row_masks = [self.row_bit_mask, ] * self.num_rows
        self.col_ones = [0, ] * len(col_clues)
        self.col_zeros = [0, ] * len(col_clues)
        self.col_masks = [self.col_bit_mask, ] * self.num_cols

        # TODO: refactor to string representation of nonogram
        self.rows = [[' ', ] * self.num_cols for _ in range(self.num_rows)]

        self.before = None
        self.backups = []

    def update_str(self):
        """
        Temporary function for refactoring.

        Convert integer nonogram to character representation.
        """
        self.rows = [[' ', ] * self.num_cols for _ in range(self.num_rows)]
        self.rows = self.transform_bin2str(self.rows,
                                           self.row_ones,
                                           self.row_zeros)

    def update_int(self):
        """
        Temporary function for refactoring.
        """
        self.row_ones = [int(''.join(row).replace(' ', '0'), 2)
                         for row in self.rows]
        self.row_zeros = [int(''.join(row).
                              replace('1', ' ').
                              replace('0', '1').
                              replace(' ', '0'), 2)
                          for row in self.rows]
        self.col_ones = [int(''.join([self.rows[row_idx][col_idx]
                                      for row_idx in range(self.num_rows)]).
                             replace(' ', '0')[::-1], 2)
                         for col_idx in range(self.num_cols)]
        self.col_zeros = [int(''.join([self.rows[row_idx][col_idx]
                                       for row_idx in range(self.num_rows)]).
                              replace('1', ' ').
                              replace('0', '1').
                              replace(' ', '0')[::-1], 2)
                          for col_idx in range(self.num_cols)]

    def transform_bin2str(self, nonogram, nonogram_ones, nonogram_zeros):
        """
        Temporary function for refactoring.
        """
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

    def rows2str(self):
        return [''.join(self.rows[row_idx])
                for row_idx in range(self.num_rows)]

    def cols2str(self):
        return [
            ''.join([row[col_idx] for row in self.rows])
            for col_idx in range(self.num_cols)]

    def set_ones_str(self, rows=None, cols=None):
        """
        Temporary function for refactoring.
        """
        if rows:
            for row_idx, row in rows:
                row = f'{row:0{self.num_cols}b}'
                for col_idx in range(self.num_cols):
                    if row[col_idx] == '1':
                        self.rows[row_idx][col_idx] = '1'
        if cols:
            for col_idx, col in cols:
                col = f'{col:0{self.num_rows}b}'
                col = col[::-1]
                for row_idx in range(self.num_rows):
                    if col[row_idx] == '1':
                        self.rows[row_idx][col_idx] = '1'
        self.update_int()


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
        self.update_str()

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
        self.update_str()

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

    def save(self):
        """
        Save a copy of the nonogram arrays.
        """
        self.before = (self.row_ones.copy(),
                       self.row_zeros.copy(),
                       self.row_masks.copy(),
                       self.col_ones.copy(),
                       self.col_zeros.copy(),
                       self.col_masks.copy(),
                       self.rows.copy())

    def has_changed(self):
        """
        Check if the nonogram has changed.
        """
        before_row_ones, before_row_zeros, _, _, _, _, _ = self.before
        return (before_row_ones != self.row_ones or
                before_row_zeros != self.row_zeros)

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
             self.col_masks.copy(),
             self.rows)
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
         self.col_masks,
         self.rows) = self.backups.pop()


class Nonogram:

    def __init__(self, clues):
        # Check which way it is faster to process the clues. Column wise or
        # row wise?
        col_clues, row_clues = clues[0], clues[1]
        total_row_variants, \
            total_col_variants = self.get_total_variants(col_clues, row_clues)
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
        self.row_idx = None
        self.varis = {}

    def get_total_variants(self, col_clues, row_clues):

        self.row_variants = sorted(num_variants(row_clues, len(col_clues)),
                                   key=lambda item: item[1])
        self.col_variants = sorted(num_variants(col_clues, len(row_clues)),
                                   key=lambda item: item[1])
        total_row_variants = functools.reduce(
            lambda x, y: x * y, [elem for _, elem in self.row_variants])
        total_col_variants = functools.reduce(
            lambda x, y: x * y, [elem for _, elem in self.col_variants])
        return total_row_variants, total_col_variants

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
        while not self.nono.complete():
            self.nono.save()
            try:
                self.deduct_positions()
            except NonogramError:
                self.nono.restore()
            if not self.nono.has_changed():
                # Get a variant for a row to get moving again.
                variant = self.next_variant(clues, max_len)
                if variant is not None:
                    self.nono.backup()
                    self.nono.set_ones(rows=[(self.row_idx, variant)])
                    self.nono.set_zeros(
                        rows=[(self.row_idx, variant ^ self.nono.row_bit_mask)])
                    # TODO: can we avoid this type of test or do it
                    #       more efficiently?
                    col_ones_str = self.nono.cols2str()
                    # TODO: temporary, fix once full str representation done
                    col_ones_str = [elem[::-1] for elem in col_ones_str]
                    if not nonogram_valid(col_ones_str, self.col_clues):
                        self.nono.restore()
                else:
                    self.nono.restore()

    def choose_row(self):
        row = None
        for idx, num in self.row_variants:
            if not self.line_complete(idx):
                row = idx
                break
        return row

    def line_complete(self, idx):
        return (self.nono.row_ones[idx] ^
                self.nono.row_zeros[idx] ^
                self.nono.row_bit_mask) == 0

    def set_common_positions(self):
        # set common positions in columns
        cols = deduct_common_positions(self.col_clues, self.nono.num_rows)
        self.nono.set_ones(cols=cols)
        # set common positions in rows
        rows = deduct_common_positions(self.row_clues, self.nono.num_cols)
        self.nono.set_ones(rows=rows)

    def deduct_positions(self):
        """
        Evaluate nonogram rows and columns.
        """
        # Deduct positions in rows.
        row_ones_str = self.nono.rows2str()
        row_ones, row_zeros = update_nonogram(row_ones_str,
                                              self.row_clues,
                                              self.nono.row_ones,
                                              self.nono.row_zeros,
                                              self.nono.row_bit_mask)
        # self.nono.set_ones(rows=row_ones)
        self.nono.set_ones_str(rows=row_ones)
        self.nono.set_zeros(rows=row_zeros)
        # Deduct positions in columns.
        col_ones_str = self.nono.cols2str()
        # TODO: temporary, fix once full str representation done
        col_ones_str = [elem[::-1] for elem in col_ones_str]
        col_ones, col_zeros = update_nonogram(col_ones_str,
                                              self.col_clues,
                                              self.nono.col_ones,
                                              self.nono.col_zeros,
                                              self.nono.col_bit_mask)
        self.nono.set_ones(cols=col_ones)
        self.nono.set_zeros(cols=col_zeros)
        # Check if the nonogram is valid.
        # TODO: Check if this test can be done better.
        row_ones_str = self.nono.rows2str()
        if not nonogram_valid(row_ones_str, self.row_clues):
            raise NonogramError
        col_ones_str = self.nono.cols2str()
        # TODO: temporary, fix once full str representation done
        col_ones_str = [elem[::-1] for elem in col_ones_str]
        if not nonogram_valid(col_ones_str, self.col_clues):
            raise NonogramError

    def next_variant(self, clues, max_len):
        self.row_idx = self.choose_row()
        if self.row_idx not in self.varis.keys():
            self.varis[self.row_idx] = combinations(self.nono,
                                                    self.row_idx,
                                                    clues, max_len)
        variant = None
        while variant is None or \
                not self.is_fitting_existing_1s(variant) or \
                not self.is_preserving_existing_1s(variant):
            # Choose a variant that matches the fields already set.
            try:
                variant = next(self.varis[self.row_idx])
            except StopIteration:
                # self.nono.restore()
                del self.varis[self.row_idx]
                self.row_idx = None
                variant = None
                break
        return variant

    def is_fitting_existing_1s(self, variant):
        """
        Check if variant fits to the existing '1's and empty positions.
        """
        return (((self.nono.row_ones[self.row_idx] |
                  self.nono.row_zeros[self.row_idx]) ^
                 self.nono.row_bit_mask) |
                self.nono.row_ones[self.row_idx]) & \
               variant == variant

    def is_preserving_existing_1s(self, variant):
        """
        Check if variant does not alternate existing '1's.
        """
        return (self.nono.row_ones[self.row_idx] & variant) == \
               self.nono.row_ones[self.row_idx]

    def show(self):
        """
        Helper function to visualize the nonogram.
        """
        reordered_col_clues = reorder(self.col_clues)
        nshow.show(self.nono.row_ones, self.nono.row_zeros,
                   reordered_col_clues, self.row_clues)


def convert_to_string(ones, zeros, num_bits):
    """
    Convert the nonogram into a string representation. Required for further
    analysis with regular expressions.
    """
    ones_str = [f'{item:0{num_bits}b}'.replace('0', ' ') for item in ones]
    zeros_str = [f'{item:0{num_bits}b}'.replace('0', ' ') for item in zeros]
    for idx_one, one in enumerate(ones_str):
        for idx_zero, char in enumerate(zeros_str[idx_one]):
            if char == '1':
                ones_str[idx_one] = ones_str[idx_one][:idx_zero] + '0' + \
                                    ones_str[idx_one][idx_zero + 1:]
    return ones_str


def update_nonogram(ones_str, clues, ones_int, zeros_int, bit_mask):
    """
    Check if nonogram is valid, deduct missing '0's and '1's.
    """
    new_ones = []
    new_zeros = []
    for idx, line in enumerate(ones_str):
        # ----- process only lines that still have gaps -----
        if ' ' not in line:
            # skip lines already completed
            continue
        # ----- if all clues set, fill rest with '0's -----
        if tuple(segment.count('1')
                 for segment in line.replace('0', ' ').split(' ')
                 if segment.count('1') > 0) == clues[idx]:
            # '1's match clues. Fill remaining positions with '0's.
            zeros = ones_int[idx] ^ bit_mask
            if zeros > 0:
                new_zeros.append((idx, zeros))
                continue
        # ----- find gaps that can be filled with '1's -----
        ones = '0' * len(line)
        # search left to right
        clues_checked = list(clues[idx])
        ones, clues_checked = gaps(line, clues[idx], 'l2r',
                                   ones, clues_checked)
        # search left to right
        ones, clues_checked = gaps(line[::-1], clues[idx][::-1], 'r2l',
                                   ones, clues_checked[::-1])
        ones = int(ones, 2)
        if ones > 0:
            new_ones.append((idx, ones))
            continue
        # ----- deduct segments that can be filled with '1's -----
        segments = get_segments(line, clues[idx])
        ones = fill_segment_1s(segments, line)
        ones = int(ones, 2)
        if ones > 0:
            new_ones.append((idx, ones))
            continue
    return new_ones, new_zeros


def gaps(line, clues, direction, ones, clues_checked):
    if clues_checked:
        line_len = len(line)
        for match in GAPS_PATTERN.finditer(line):
            if direction == 'l2r':
                start, end = match.start(), match.end()
            if direction == 'r2l':
                start, end = line_len - match.end(), line_len - match.start()
            length = end - start
            if length < clues_checked[0]:
                continue
            if length == clues_checked[0] and \
                    '1' in match.group() and \
                    ' ' in match.group():
                clues_checked.pop(0)
                ones = ones[:start] + '1' * length + ones[start + length:]
            elif length == clues_checked[0] and \
                    '1' in match.group() and \
                    ' ' not in match.group():
                clues_checked.pop(0)
            else:
                # Stop searching. The gap is either bigger than the given clue
                # or doesn't contain a '1'.
                break
            if not clues_checked:
                break
    return ones, clues_checked


def get_segments(line, clues):
    line_len = len(line)
    # get segments doing regex left to right
    segments_pat_l2r = re.compile(detect_segments_pattern(clues))
    segments_l2r = segments_pat_l2r.match(line)
    if not segments_l2r:
        raise NonogramError  # The nonogram is invalid.
    segments_l2r = [
        (segments_l2r.start(grp_num),
         segments_l2r.end(grp_num))
        for grp_num in range(1, len(segments_l2r.groups()) + 1)]
    # get segments doing regex right to left
    segments_pat_r2l = re.compile(detect_segments_pattern(clues[::-1]))
    segments_r2l = segments_pat_r2l.match(line[::-1])
    segments_r2l = [
        (line_len - segments_r2l.start(grp_num),
         line_len - segments_r2l.end(grp_num))
        for grp_num in range(1, len(segments_r2l.groups()) + 1)]
    segments_r2l = [elem[::-1]
                    for elem in segments_r2l][::-1]
    # calculate the overlap between the segments
    segments = [
        (segments_r2l[seg_idx][0],
         segments_l2r[seg_idx][1])
        for seg_idx in range(len(segments_l2r))
        if segments_r2l[seg_idx][0] < segments_l2r[seg_idx][1]]
    return segments


def fill_segment_1s(segments, line):
    ones = '0' * len(line)
    for start, end in segments:
        length = end - start
        if '1' in line[start:end] and ' ' in line[start:end]:
            ones = ones[:start] + '1' * length + ones[start + length:]
    return ones


def nonogram_valid(ones_str, clues):
    for idx, line in enumerate(ones_str):
        segments_pattern = re.compile(detect_segments_pattern(clues[idx]))
        segments_match = segments_pattern.match(line)
        if not segments_match:
            return False
    return True


def detect_segments_pattern(clue):
    pattern = [r'([1 ]{' + str(num) + '})' for num in clue]
    pattern = '[0 ]+?'.join(pattern)
    pattern = '^[0 ]*?' + pattern + '[0 ]*?$'
    return pattern


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


def transpose(items, max_len):
    new_rows = []
    for col_idx in reversed(range(max_len)):
        new_rows.append(sum(
            [((item & (1 << col_idx)) >> col_idx) << (max_len - row_idx - 1)
             for row_idx, item in enumerate(items)])
        )
    return new_rows


def bin2tuple(nonogram_ones, num_cols):
    fmt = '{0:0' + str(num_cols) + 'b}'
    nonogram = tuple(
        tuple(int(cell) for cell in fmt.format(item)) for item in nonogram_ones
    )
    return nonogram


if __name__ == '__main__':
    test_clues = (
        ((1, 1), (4,), (1, 1, 1), (3,), (1,)),
        ((1,), (2,), (3,), (2, 1), (4,)))
    nonogram = Nonogram(test_clues)
    sol = nonogram.solve()
    print(sol)
