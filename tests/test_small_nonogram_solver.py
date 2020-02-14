"""

Test suite for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

"""

import pytest
from solutions.small_nonogram_solver import Nonogram


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
]


@pytest.mark.parametrize('test', TESTS)
def test_nonograms(test):
    """ tests """
    clues = test['clues']
    ans = test['ans']
    assert ans == Nonogram(clues).solve()
