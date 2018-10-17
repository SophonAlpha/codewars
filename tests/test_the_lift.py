"""
Test suite for The Lift kata:
https://www.codewars.com/kata/the-lift
"""

import pytest

from solutions.the_lift import Dinglemouse
from solutions.the_lift import is_tuple_empty

# Floors:    G   1      2        3   4     5     6     Answers:
tests = [[ ( (), (),    (5,5,5), (), (),   (),   () ), [0, 2, 5, 0]         ],
         [ ( (), (),    (1,1),   (), (),   (),   () ), [0, 2, 1, 0]         ],
         [ ( (), (3,),  (4,),    (), (5,), (),   () ), [0, 1, 2, 3, 4, 5, 0]],
         [ ( (), (0,),  (),      (), (2,), (3,), () ), [0, 5, 4, 3, 2, 1, 0]],
         [ ( (), (),    (),      (), (),   (),   () ), [0]                  ]]

@pytest.mark.parametrize('queues, answer', tests)
def test_cases(queues, answer):
    lift = Dinglemouse(queues, 5)
    assert lift.theLift() == answer

@pytest.mark.parametrize('queues, answer', tests)
def test_func_is_empty(queues, answer):
    assert is_tuple_empty(queues) == (answer == [0])
