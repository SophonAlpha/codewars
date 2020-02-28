"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""

import functools


class Nonogram:

    def __init__(self, clues):
        self.clues = clues
        self.nonogram = [['?',] * len(self.clues[0]) for _ in self.clues[1]]
        self.num_cols = len(self.clues[0])

    def solve(self):
        cols = common_positions(self.clues[0])
        cols = transpose_bitwise(cols)
        rows = common_positions(self.clues[1])
        self.set_ones(combine(rows, cols))
        print('\nnonogram:\n')
        print(f'cols: {self.clues[0]}')
        print(f'rows: {self.clues[1]}')
        print()
        for line in self.nonogram:
            print(line)
        self.set_zeros()
        print()
        for line in self.nonogram:
            print(line)
        return self.nonogram

    def set_ones(self, int_nonogram):
        fmt = '{0:0' + str(self.num_cols) + 'b}'
        for row, item in enumerate(int_nonogram):
            for col, cell in enumerate(fmt.format(item)):
                self.nonogram[row][col] = cell if cell == '1' \
                    else self.nonogram[row][col]

    def set_zeros(self):
        for col, col_clues in enumerate(self.clues[0]):
            nono_col_sum = sum([1 if row[col] == '1' else 0
                                for row in self.nonogram])
            if nono_col_sum == sum(col_clues):
                for row, _ in enumerate(self.nonogram):
                    if self.nonogram[row][col] == '?':
                        self.nonogram[row][col] = '0'

        for row, row_clues in enumerate(self.clues[1]):
            nono_row_sum = sum([1 if col == '1' else 0
                                for col in self.nonogram[row]])
            if nono_row_sum == sum(row_clues):
                for col, _ in enumerate(self.nonogram[row]):
                    if self.nonogram[row][col] == '?':
                        self.nonogram[row][col] = '0'


def common_positions(clues):
    items = []
    for common_positions in combinations(clues):
        items.append(common_positions)
    return items


def combinations(clues):
    max_len = len(clues)
    fmt = '{0:0' + str(max_len) + 'b}'
    for clue in clues:
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        clue_shftd = init_shift(clue, max_len)
        for combination in combinator(clue_shftd, 0, 0, max_r_shift):
            print(fmt.format(or_merge(combination)))

        # positions = get_combinations(clue_shftd, 0, 0, max_r_shift)
        common_positions = and_merge(positions)
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


def transpose(items, max_len):
    items_transposed = []
    fmt = '{0:0' + str(max_len) + 'b}'
    for idx in range(max_len):
        transposed = [fmt.format(item)[idx] for item in items]
        transposed = int('0b' + ''.join(transposed), base=2)
        items_transposed.append(transposed)
    return items_transposed


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


def combinator_v1(clue, max_r_shift):
    clue_shftd = clue[:]
    r_shift = [1] * (len(clue) - 1)
    r_shift.append(0)
    idx = len(clue) - 1
    while idx >= 0:
        if r_shift[idx] <= max_r_shift:
            clue_shftd[idx] = clue[idx] >> r_shift[idx]
            yield clue_shftd
            r_shift[idx] += 1
        if r_shift[idx] > max_r_shift:
            # r_shift[idx - 1] += 1
            clue_shftd[idx] = clue[idx] >> r_shift[idx - 1]
            r_shift[idx] = r_shift[idx - 1]
            idx -= 1
        elif idx < len(clue) - 1:
            idx += 1
            r_shift[idx] += 1


def set_zeros(nonogram_ones):
    return


if __name__ == '__main__':
    clues = (((1, 2, 1), (4,), (1, 1, 1), (3,), (1,), (1,), (1,), (1,), (1,)),
             ((1,), (2,), (3,), (2, 1), (4,)))
    ans = ((0, 0, 1, 0, 0),
           (1, 1, 0, 0, 0),
           (0, 1, 1, 1, 0),
           (1, 1, 0, 1, 0),
           (0, 1, 1, 1, 1))
    sol = Nonogram(clues).solve()
    print()
