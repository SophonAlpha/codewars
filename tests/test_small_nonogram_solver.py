"""

Test suite for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

"""

import pytest
import random
from solutions.medium_nonogram_solver import Nonogram
from solutions.medium_nonogram_solver import combinator
from solutions.medium_nonogram_solver import init_shift


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
    {'clues': (((3, 1), (2, 1), (3, 1), (1, 1, 2), (2, 1), (1, 1), (1, 1, 1)),
               ((2, 1, 1), (3,), (1, 1, 1), (3,), (1, 2), (1, 3), (1, 2))),
     'ans': ((1, 1, 0, 1, 0, 0, 1),
             (1, 1, 1, 0, 0, 0, 0),
             (1, 0, 1, 0, 1, 0, 0),
             (0, 0, 1, 1, 1, 0, 0),
             (0, 1, 0, 0, 0, 1, 1),
             (1, 0, 1, 1, 1, 0, 0),
             (0, 0, 0, 1, 0, 1, 1))},
    {'clues': (((2, 1), (1,), (1, 1, 1), (1, 1), (3,), (2, 2), (4, 1)),
               ((1, 2, 1), (1, 2), (1, 1), (1, 1, 1), (1, 3), (3,), (1, 1))),
     'ans': ((1, 0, 1, 1, 0, 1, 0),
             (1, 0, 0, 0, 0, 1, 1),
             (0, 0, 1, 0, 0, 0, 1),
             (1, 0, 0, 0, 1, 0, 1),
             (0, 0, 1, 0, 1, 1, 1),
             (0, 0, 0, 1, 1, 1, 0),
             (0, 1, 0, 0, 0, 0, 1))},
]

PERFORMANCE_TESTS = [
    {'clues': (
        ((1, 1, 1), (1, 2, 3), (1, 4), (2, 1),
         (1, 2, 3), (1, 1, 1), (1, 2), (1,)),
        ((1, 2), (1, 2), (2, 2), (1, 3),
         (1, 1), (2, 1, 1), (2, 3), (5,))
    ),
        'ans': ((0, 1, 0, 0, 1, 1, 0, 0),
                (0, 0, 1, 0, 0, 0, 1, 1),
                (1, 1, 0, 1, 1, 0, 0, 0),
                (0, 1, 0, 1, 1, 1, 0, 0),
                (1, 0, 1, 0, 0, 0, 0, 0),
                (0, 1, 1, 0, 1, 0, 1, 0),
                (0, 1, 1, 0, 1, 1, 1, 0),
                (1, 1, 1, 1, 1, 0, 0, 0))},
    {'clues': (((1, 1, 2), (1, 1, 1), (1, 1, 1), (5,),
                (3, 1), (1, 1), (1, 1, 2, 1), (1, 3, 2)),
               ((2, 2), (1, 1), (1, 2), (2, 2, 1),
                (3, 2), (1, 1, 1), (2, 1, 1, 1), (3, 2))),
     'ans': (
         (0, 1, 1, 0, 0, 0, 1, 1),
         (1, 0, 0, 0, 0, 1, 0, 0),
         (0, 0, 0, 0, 1, 0, 1, 1),
         (1, 1, 0, 1, 1, 0, 0, 1),
         (0, 0, 1, 1, 1, 0, 1, 1),
         (1, 0, 0, 1, 0, 0, 1, 0),
         (1, 1, 0, 1, 0, 1, 0, 1),
         (0, 0, 1, 1, 1, 0, 1, 1))},
    {'clues': (((1, 1, 1), (2, 2), (3, 2), (3, 1),
                (1, 2), (1, 1, 2), (1, 1, 1), (3, 1)),
               ((1, 1, 2), (1, 1), (6,), (1, 1),
                (3, 2), (2, 1, 1), (1, 2), (1, 3))),
     'ans': ((1, 0, 0, 1, 0, 1, 1, 0),
             (0, 1, 0, 1, 0, 0, 0, 0),
             (1, 1, 1, 1, 1, 1, 0, 0),
             (0, 0, 1, 0, 0, 0, 0, 1),
             (0, 1, 1, 1, 0, 0, 1, 1),
             (1, 1, 0, 0, 1, 0, 0, 1),
             (0, 0, 1, 0, 1, 1, 0, 0),
             (0, 0, 1, 0, 0, 1, 1, 1))}
]


# --------- support functions --------------------------------------------------


def wrapper(func, *args, **kwargs):
    """
    Wrapper function for performance testing individual functions.
    """
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def random_nonograms(num_cols=5, num_rows=5, num_test=10):
    for idx in range(num_test):
        clues, ans = generate_nonogram(num_cols, num_rows)
        yield clues, ans


def count_variants(clues, max_len):
    num_variants_comb = []
    num_variants_counts = []
    for clue in clues:
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        clue_shftd = init_shift(clue, max_len)
        combinations = list(combinator(clue_shftd, 0, 0, max_r_shift))
        num_variants_comb.append(combinations)
        num_variants_counts.append(len(combinations))
    return num_variants_counts


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


# ---------- test functions ----------------------------------------------------


@pytest.mark.parametrize('test', random_nonograms(num_cols=25,
                                                  num_rows=25,
                                                  num_test=50))
def test_num_variants(test):
    """
    Test to ensure that the function for calculating the number of clue variants
    is correct. We compare calculated variants against the number of all
    possible combinations.
    """
    start_clues = test[0]
    nono = Nonogram(start_clues)
    num_row_variants_counts = count_variants(nono.row_clues, nono.num_cols)
    assert nono.num_row_variants == num_row_variants_counts
    num_col_variants_counts = count_variants(nono.col_clues, nono.num_rows)
    assert nono.num_col_variants == num_col_variants_counts


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


@pytest.mark.parametrize('test', random_nonograms(num_cols=9,
                                                  num_rows=9,
                                                  num_test=100))
def test_random_nonograms(test):
    """ tests """
    clues_test = test[0]
    ans = test[1]
    # print()
    # print(f'clues = {clues_test}')
    # print()
    # print(f'ans = {ans}')
    num_cols = len(test[1])
    nonogram_ones = tuple2bin(Nonogram(clues_test).solve())
    row_clues, col_clues = get_clues(nonogram_ones, num_cols)
    col_clues = tuple(clue[::-1] for clue in col_clues)
    clues_ans = (col_clues, row_clues)
    assert clues_ans == clues_test


@pytest.mark.parametrize('test', random_nonograms(num_cols=25,
                                                  num_rows=25,
                                                  num_test=50))
def test_combinator_speed(test):
    """ test """
    col_clues, row_clues = test[0][0], test[0][1]
    max_len = len(col_clues)
    print()
    for clue in row_clues:
        max_r_shift = max_len - (sum(clue) + len(clue) - 1)
        clue_shftd = init_shift(clue, max_len)
        count = 0
        for _ in combinator(clue_shftd, 0, 0, max_r_shift):
            count += 1
        print(f'{clue}: {count:,}')


@pytest.mark.parametrize('test', PERFORMANCE_TESTS)
def test_performance(test):
    """
    Performance profiling
    """
    import cProfile, pstats, sys
    clues_test = test['clues']
    num_cols = len(test['ans'][0])
    profile = cProfile.Profile()
    profile.enable()
    nonogram_ones = Nonogram(clues_test).solve()
    profile.disable()
    ps = pstats.Stats(profile, stream=sys.stdout).strip_dirs().sort_stats(
        pstats.SortKey.CUMULATIVE)
    print()
    ps.print_stats('medium_nonogram_solver.py:')
    nonogram_ones = tuple2bin(nonogram_ones)
    row_clues, col_clues = get_clues(nonogram_ones, num_cols)
    col_clues = tuple(clue[::-1] for clue in col_clues)
    clues_ans = (col_clues, row_clues)
    assert clues_ans == clues_test
