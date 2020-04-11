"""

Test suite for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

"""

import pytest
from solutions.small_nonogram_solver import Nonogram
# from solutions.medium_nonogram_solver import Nonogram
import random

TESTS = [
    {'clues': (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
               ((1,), (2,), (3,), (2, 1), (4,))),
     'ans': ((0, 0, 1, 0, 0),
             (1, 1, 0, 0, 0),
             (0, 1, 1, 1, 0),
             (1, 1, 0, 1, 0),
             (0, 1, 1, 1, 1))},
    {'clues': (((1,), (3,), (1,), (3, 1), (3, 1)),
               ((3,), (2,), (2, 2), (1,), (1, 2))),
     'ans': ((0, 0, 1, 1, 1),
             (0, 0, 0, 1, 1),
             (1, 1, 0, 1, 1),
             (0, 1, 0, 0, 0),
             (0, 1, 0, 1, 1))},
    {'clues': (((3,), (2,), (1, 1), (2,), (4,)),
               ((2,), (3, 1), (1, 2), (3,), (1,))),
     'ans': ((1, 1, 0, 0, 0),
             (1, 1, 1, 0, 1),
             (1, 0, 0, 1, 1),
             (0, 0, 1, 1, 1),
             (0, 0, 0, 0, 1))},
    {'clues': (((1,), (1, 1), (2,), (1, 2), (1, 1)),
               ((1,), (1, 1), (1,), (4,), (2,))),
     'ans': ((0, 0, 0, 0, 1),
             (0, 1, 0, 1, 0),
             (0, 0, 0, 0, 1),
             (1, 1, 1, 1, 0),
             (0, 0, 1, 1, 0))},
    {'clues': (((1,), (1,), (1,), (4,), (2,)),
               ((1,), (1, 1), (1,), (1, 2), (1, 1))),
     'ans': ((0, 0, 0, 1, 0),
             (1, 0, 0, 1, 0),
             (0, 0, 0, 1, 0),
             (0, 1, 0, 1, 1),
             (0, 0, 1, 0, 1))},
    {'clues': (((1, 1), (1, 1), (1, 1), (2, 1), (2, 1)),
               ((1, 3), (1, 2), (0,), (4,), (1,))),
     'ans': ((1, 0, 1, 1, 1),
             (0, 1, 0, 1, 1),
             (0, 0, 0, 0, 0),
             (1, 1, 1, 1, 0),
             (0, 0, 0, 0, 1))},
    # {'clues': (((3, 1), (2, 1), (3, 1), (1, 1, 2), (2, 1), (1, 1), (1, 1, 1)),
    #            ((2, 1, 1), (3,), (1, 1, 1), (3,), (1, 2), (1, 3), (1, 2))),
    #  'ans': ((1, 1, 0, 1, 0, 0, 1),
    #          (1, 1, 1, 0, 0, 0, 0),
    #          (1, 0, 1, 0, 1, 0, 0),
    #          (0, 0, 1, 1, 1, 0, 0),
    #          (0, 1, 0, 0, 0, 1, 1),
    #          (1, 0, 1, 1, 1, 0, 0),
    #          (0, 0, 0, 1, 0, 1, 1))},
]


def random_nonograms():
    num_cols = 5
    num_rows = 5
    num_test = 150
    for idx in range(num_test):
        clues, ans = generate_nonogram(num_cols, num_rows)
        yield clues, ans


@pytest.mark.parametrize('test', TESTS)
def test_nonograms(test):
    """ tests """
    clues_test = test['clues']
    num_cols = len(test['ans'][0])
    nonogram_ones = tuple2bin(Nonogram(clues_test).solve())
    row_clues, col_clues = get_clues(nonogram_ones, num_cols)
    col_clues = tuple(clue[::-1] for clue in col_clues)
    clues_ans = (col_clues, row_clues)
    assert clues_ans == clues_test


@pytest.mark.parametrize('test', random_nonograms())
def test_random_nonograms(test):
    """ tests """
    clues_test = test[0]
    num_cols = len(test[1])
    nonogram_ones = tuple2bin(Nonogram(clues_test).solve())
    row_clues, col_clues = get_clues(nonogram_ones, num_cols)
    col_clues = tuple(clue[::-1] for clue in col_clues)
    clues_ans = (col_clues, row_clues)
    assert clues_ans == clues_test


def generate_nonogram(num_cols, num_rows):
    nonogram_ones = [random.randrange(2 ** num_cols) for _ in range(num_rows)]
    row_clues, col_clues = get_clues(nonogram_ones, num_cols)
    col_clues = tuple(clue[::-1] for clue in col_clues)
    clues = (col_clues, row_clues)
    ans = bin2tuple(nonogram_ones, num_cols)
    return clues, ans


def get_clues(nonogram_ones, num_cols):
    row_clues = get_clues_count(nonogram_ones, num_cols)
    col_clues = get_clues_count(cols2rows(nonogram_ones, num_cols), num_cols)
    return row_clues, col_clues


def get_clues_count(nonogram_ones, num_cols):
    fmt = '{0:0' + str(num_cols) + 'b}'
    clues_count = tuple(
        tuple(
            item.count('1')
            for item in fmt.format(row).strip('0').split('0')
        )
        for row in nonogram_ones
    )
    clues_count = tuple(clue if len(clue) <= 2 else
                        clue[:1] +
                        tuple(item for item in clue[1:-1] if item != 0) +
                        clue[-1:]
                        for clue in clues_count)
    return clues_count


def cols2rows(items, max_len):
    new_rows = []
    for idx in reversed(range(max_len)):
        new_rows.append(sum([((item & (1 << idx)) >> idx) << pos
                             for pos, item in enumerate(items)]))
    return new_rows


def bin2tuple(nonogram_ones, num_cols):
    fmt = '{0:0' + str(num_cols) + 'b}'
    nonogram = tuple(
        tuple(int(cell) for cell in fmt.format(item))
        for item in nonogram_ones)
    return nonogram


def tuple2bin(nonogram):
    nonogram_ones = [int(''.join([str(item) for item in row]), 2)
                     for row in nonogram]
    return nonogram_ones
