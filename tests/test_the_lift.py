"""
Test suite for The Lift kata:
https://www.codewars.com/kata/the-lift
"""

import pytest

from solutions.the_lift import Dinglemouse

TESTS = [[((), (), (5, 5, 5), (), (), (), ()), [0, 2, 5, 0]],
         [((), (), (1, 1), (), (), (), ()), [0, 2, 1, 0]],
         [((), (3,), (4,), (), (5,), (), ()), [0, 1, 2, 3, 4, 5, 0]],
         [((), (0,), (), (), (2,), (3,), ()), [0, 5, 4, 3, 2, 1, 0]],
         [((), (), (), (), (), (), ()), [0]]]

@pytest.mark.parametrize('queues, answer', TESTS)
def test_cases(queues, answer):
    """ test """
    lift = Dinglemouse(queues, 5)
    assert lift.theLift() == answer
