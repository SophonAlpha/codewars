"""
Solution for Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/

test Sonarlint: https://www.sonarlint.org/
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


class NonogramError(Exception):
    """
    Custom error class: thrown when the '1s' set in the nonogram don't macth the
    row clues or column clues.
    """


class Nonogram:

    def __init__(self, clues):
        self.col_clues, self.row_clues = reorder(clues[0]), clues[1]
        self.nonogram_ones = [0, ] * len(self.row_clues)
        self.nonogram_zeros = [0, ] * len(self.row_clues)
        self.store = []
        self.rows_save = None
        self.num_cols = len(self.col_clues)
        self.num_rows = len(self.row_clues)
        self.col_bit_mask = 2 ** self.num_cols - 1
        self.row_bit_mask = 2 ** self.num_rows - 1
        self.nonogram_col_masks = [self.col_bit_mask, ] * self.num_cols
        self.nonogram_masks = [self.row_bit_mask, ] * self.num_rows
        self.num_row_variants = num_variants(self.row_clues, self.num_cols)
        self.num_col_variants = num_variants(self.col_clues, self.num_rows)
        self.row_combinators = init_combinator(self.row_clues,
                                               self.num_cols)
        self.row_selector = [True, ] * self.num_rows
        self.col_combinators = init_combinator(self.col_clues,
                                               self.num_rows)
        self.col_selector = [True, ] * self.num_cols
        self.row_or_col = None

    def solve(self):
        rows = [0] * self.num_rows
        cols = [0] * self.num_cols
        idx_min_row = self.num_row_variants.index(min(
            itertools.compress(self.num_row_variants, self.row_selector)))
        idx_min_col = self.num_col_variants.index(min(
            itertools.compress(self.num_col_variants, self.col_selector)))
        if not self.row_or_col:
            if self.num_row_variants[idx_min_row] <= self.num_col_variants[
                idx_min_col]:
                # choose a row variant
                self.row_or_col = "row"
            else:
                # choose column variants
                self.row_or_col = "col"
        if self.row_or_col == "row":
            clues = self.row_clues[idx_min_row]
            max_len = self.num_cols
            for clue in clues:
                max_r_shift = max_len - (sum(clue) + len(clue) - 1)
                clue_shftd = init_shift(clue, max_len)
                combination = combinator(clue_shftd, 0, 0, max_r_shift)





        elif self.row_or_col == "col":



        return rows

        for clue in clues:
            max_r_shift = max_len - (sum(clue) + len(clue) - 1)
            clue_shftd = init_shift(clue, max_len)
            wrapped = wrapper(combinator, clue_shftd, 0, 0, max_r_shift)
            combinator_funcs.append(wrapped())

    def solve_v1(self):
        while not self.is_solved():
            prev_ones = self.nonogram_ones[:]
            prev_zeros = self.nonogram_zeros[:]
            # # set common positions in columns
            # cols = find_common_positions(self.col_clues,
            #                              self.nonogram_col_masks,
            #                              self.num_rows)
            # cols = rows2cols(cols, len(cols))
            # self.set_ones(cols)
            # self.set_zeros()
            # self.update_nonogram_mask()
            # # set common positions in rows
            # rows = find_common_positions(self.row_clues,
            #                              self.nonogram_masks,
            #                              self.num_cols)
            # self.set_ones(rows)
            # self.set_zeros()
            # self.update_nonogram_mask()
            # # set fixed positions in columns
            # cols = find_fixed_positions(self.col_clues, cols2rows(
            #     self.nonogram_col_masks, self.num_rows), cols2rows(
            #     self.nonogram_ones, self.num_rows))
            # rows = rows2cols(cols, len(cols))
            # self.set_ones(rows)
            # self.set_zeros()
            # self.update_nonogram_mask()
            # # set fixed positions in rows
            # rows = find_fixed_positions(self.row_clues, self.nonogram_masks,
            #                             self.nonogram_ones)
            # self.set_ones(rows)
            # self.set_zeros()
            # self.update_nonogram_mask()
            # check if reached a state of no progress
            if not self.is_solved() and \
                    not progress(prev_ones, self.nonogram_ones,
                                 prev_zeros, self.nonogram_zeros):
                self.save_selectors()
                try:
                    rows = self.choose_combination()
                except StopIteration:
                    self.restore_selectors()
                    # two restores are needed
                    self.restore()
                    self.restore()
                    self.update_nonogram_mask()
                else:
                    self.save_nonogram()
                    self.set_ones(rows)
                    self.set_zeros()
                    self.update_nonogram_mask()
            # check that the nonogram is consistent ('1s' match the clues)
            try:
                self.check()
            except NonogramError:
                self.restore()
                self.update_nonogram_mask()
        return bin2tuple(self.nonogram_ones, self.num_cols)

    def is_solved(self):
        return sum(self.nonogram_masks) + sum(self.nonogram_col_masks) == 0

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

        # self.nonogram_masks = [
        #     mask | self.nonogram_ones[idx] if mask != 0 else mask
        #     for idx, mask in enumerate(self.nonogram_masks)
        # ]
        # # column wise add all set positions ("1s")
        # self.nonogram_col_masks = cols2rows(ones_zeros[:], self.num_cols)
        # col_ones = cols2rows(self.nonogram_ones, self.num_cols)
        # self.nonogram_col_masks = [
        #     mask | col_ones[idx] if mask != 0 else mask
        #     for idx, mask in enumerate(self.nonogram_col_masks)
        # ]

    # def set_one_position(self):
    #     rows = [0] * self.num_rows
    #     row_open_positions = [ones | self.nonogram_zeros[idx]
    #                           for idx, ones in enumerate(self.nonogram_ones)]
    #     col_open_positions = cols2rows(row_open_positions, self.num_cols)
    #     row_counts = [(idx, f'{item:0{self.num_cols}b}'.count('0'))
    #                   for idx, item in enumerate(row_open_positions)
    #                   if self.nonogram_row_masks[idx] != 0]
    #     col_counts = [(idx, f'{item:0{self.num_cols}b}'.count('0'))
    #                   for idx, item in enumerate(col_open_positions)
    #                   if self.nonogram_col_masks[idx] != 0]
    #     row_index, row_num_zeros = min(row_counts,
    #                                    key=operator.itemgetter(1))
    #     col_index, col_num_zeros = min(col_counts,
    #                                    key=operator.itemgetter(1))
    #     if row_num_zeros <= col_num_zeros:
    #         bit_pos = get_first_zero_bit(row_open_positions[row_index],
    #                                      self.num_cols)
    #         rows[row_index] = 1 << bit_pos
    #     else:
    #         bit_pos = get_first_zero_bit(col_open_positions[col_index],
    #                                      self.num_cols)
    #         rows[bit_pos] = 1 << (self.num_cols - 1 - col_index)
    #     return rows

    def choose_combination(self):
        rows = [0] * self.num_rows
        cols = [0] * self.num_cols
        idx_min_row = self.num_row_variants.index(min(
            itertools.compress(self.num_row_variants, self.row_selector)
        )
        )
        idx_min_col = self.num_col_variants.index(min(
            itertools.compress(self.num_col_variants, self.col_selector)
        )
        )
        if not self.row_or_col:
            if self.num_row_variants[idx_min_row] <= self.num_col_variants[
                idx_min_col]:
                # choose a row variant
                self.row_or_col = "row"
            else:
                # choose column variants
                self.row_or_col = "col"
        if self.row_or_col == "row":
            # choose a row variant
            found = False
            while not found:
                combination = next(self.row_combinators[idx_min_row])
                found = rows[idx_min_row] & combination == rows[idx_min_row]
            rows[idx_min_row] = combination
            self.row_selector[idx_min_row] = False
        elif self.row_or_col == "col":
            # choose a column variant
            columns = cols2rows(self.nonogram_ones, self.num_cols)
            found = False
            while not found:
                combination = next(self.col_combinators[idx_min_col])
                found = columns[idx_min_col] & combination == columns[
                    idx_min_col]
            cols[idx_min_col] = combination
            rows = rows2cols(cols, self.num_rows)
            self.col_selector[idx_min_col] = False
        return rows

    # def get_col_masks(self):
    #     return self.nonogram_col_masks[:]
    #
    # def get_row_masks(self):
    #     return self.nonogram_row_masks[:]

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
        width = self.num_rows
        new_col_zeros = set_new_zeros(ones, width, self.col_clues)
        new_col_zeros = rows2cols(new_col_zeros, self.num_rows)
        # set zeros in rows
        new_row_zeros = set_new_zeros(self.nonogram_ones, self.num_cols,
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

    def save_selectors(self):
        """
        Save the current state of the nonogram row and column selectors.
        """
        self.store.append((self.row_selector[:],
                           self.col_selector[:],))

    def restore_selectors(self):
        (self.row_selector,
         self.col_selector,) = self.store.pop()

    def save_nonogram(self):
        """
        Save the current state of the nonogram.
        """
        # save the current state of the row and column variants iterators
        row_iter_states = [itertools.tee(iter_state)
                           for iter_state in self.row_combinators]
        col_iter_states = [itertools.tee(iter_state)
                           for iter_state in self.col_combinators]
        # save the nonogram details in a list
        self.store.append((self.nonogram_ones[:],
                           self.nonogram_zeros[:],
                           self.nonogram_masks[:],
                           row_iter_states,
                           col_iter_states,
                           self.row_or_col,))

    def restore(self):
        # restore the nonogram details
        (self.nonogram_ones,
         self.nonogram_zeros,
         self.nonogram_masks,
         row_iter_states,
         col_iter_states,
         self.row_or_col,) = self.store.pop()
        # restore the row and column selectors
        (self.row_selector,
         self.col_selector,) = self.store.pop()
        # restore the states of the row and column variants iterators
        self.row_combinators = [prev_state
                                for prev_state, _ in row_iter_states]
        self.col_combinators = [prev_state
                                for prev_state, _ in col_iter_states]

    def set_failed_to_zero(self, rows):
        idx, value = max(enumerate(rows), key=operator.itemgetter(1))
        self.nonogram_zeros[idx] = self.nonogram_zeros[idx] | value

    def check(self):
        # TODO: refactor to reduce duplication of code for rows and columns
        # check that there is no overlap between the "ones" map and the "zeros"
        # map. If there is, this indicates that a choosen variant has
        # overwritten an already found "zero".
        separate = [
            row ^ self.nonogram_zeros[idx] == row | self.nonogram_zeros[idx]
            for idx, row in enumerate(self.nonogram_ones)
        ]
        if not all(separate):
            raise NonogramError('Overlap between the \'one\' and '
                                '\'zero\' maps.')
        # check row '1s' match row clues
        length = self.num_cols
        row_clues = tuple((tuple(clue.count('1')
                                 for clue in f'{row:0{length}b}'.split('0')
                                 if clue)
                           for row in self.nonogram_ones))
        row_clues = tuple(clue if clue else (0,) for clue in row_clues)
        rows_ok = [False if self.nonogram_masks[idx] == 0 and
                            item != self.row_clues[idx] else True
                   for idx, item in enumerate(row_clues)]
        if not all(rows_ok):
            raise NonogramError('Set "1s" in the nonogram rows '
                                'don\'t match the row clues.')
        # check column '1s' match column clues
        length = self.num_rows
        col_clues = tuple((tuple(clue.count('1')
                                 for clue in f'{col:0{length}b}'.split('0')
                                 if clue)
                           for col in cols2rows(self.nonogram_ones,
                                                self.num_cols)))
        col_clues = tuple(clue if clue else (0,) for clue in col_clues)
        cols_ok = [False if self.nonogram_col_masks[idx] == 0 and
                            item != self.col_clues[idx] else True
                   for idx, item in enumerate(col_clues)]
        if not all(cols_ok):
            raise NonogramError('Set "1s" in the nonogram columns '
                                'don\'t match the column clues.')


def init_combinator(clues, max_len):
    combinator_funcs = []
    for clue in clues:
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        clue_shftd = init_shift(clue, max_len)
        wrapped = wrapper(combinator, clue_shftd, 0, 0, max_r_shift)
        combinator_funcs.append(wrapped())
    return combinator_funcs


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


def find_common_positions_v1(clues, pos_masks, max_len):
    items = [0, ] * max_len
    for idx, clue, mask in [(idx, clue, pos_masks[idx])
                            for idx, clue in enumerate(clues)]:
        if mask != 0:
            items[idx] = combinations(clue, mask, max_len)
    return items


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


def combinations(clue, mask, max_len):
    # TODO: for performance optimisation add a test for checking that the mask
    #       length is bigger than minimum length of the bit combination based
    #       on the clue. For example: mask with only two bits '11' but clue is
    #       (1, 1) which requires minimum 3 bits '101'.
    cmn_positions = None
    max_r_shift = max_len - (sum(clue) + len(clue) - 1)
    clue_shftd = init_shift(clue, max_len)
    for combination in combinator(clue_shftd, 0, 0, max_r_shift):
        if (combination & mask == combination) and (cmn_positions is None):
            # store very first value
            cmn_positions = combination
        if (combination & mask == combination) and cmn_positions:
            # bitwise 'and' with any subsequent value
            cmn_positions = and_merge([cmn_positions, combination])
        if cmn_positions == 0:
            break
    cmn_positions = 0 if cmn_positions is None else cmn_positions
    return cmn_positions


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


def set_new_zeros(ones, width, clues):
    """
    Set the zeros for a nonogram array. The algorithm looks for the segments of
    '1s' and compares against the given clues. Where the number of '1s' matches
    the clue set the positions left and right to the '1s' to '0'.
    """
    new_zeros = [0] * len(ones)
    for idx, line in enumerate(ones):
        segments = tuple(item.count('1')
                         for item in f'{line:0{width}b}'.split('0')
                         if item)
        # Check if reminder of line can be set to zero.
        if sum(segments) == sum(clues[idx]):
            # All clues found! Mark all remaining positions as zeros.
            new_zeros[idx] = (2 ** width - 1) ^ line
        # elif len(segments) == len(clues[idx]):
        #     # Check if positions next to '1s' can be set to '0'.
        #     line_clues = clues[idx]
        #     new_zeros[idx] = find_neighbour_zeros(line, segments,
        #                                           line_clues, width)
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


def progress(prev_ones, nonogram_ones, prev_zeros, nonogram_zeros):
    return prev_ones != nonogram_ones or prev_zeros != nonogram_zeros


def get_first_zero_bit(value, max_len):
    bit_pos = None
    for pos in range(max_len):
        mask = 1 << pos
        if value & mask == 0:
            bit_pos = pos
            break
    return bit_pos


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
    print(sol == ans)
    pprint.pprint(sol)
    print()
    pprint.pprint(ans)
