"""

Test suite Become Immortal kata:
https://www.codewars.com/kata/become-immortal

"""

import pytest

from solutions.become_immortal import elder_age

TESTS = [(8, 5, 1, 100, 5),
         (7, 4, 1, 100, 66),
         (8, 8, 0, 100007, 224),
         (25, 31, 0, 100007, 11925),
         (5, 45, 3, 1000007, 4323),
         (31, 39, 7, 2345, 1586),
         (545, 435, 342, 1000007, 808451),
         (28827050410, 35165045587, 7109602, 13719506, 5456283)]

@pytest.mark.parametrize('m, n, l, t, correct_age', TESTS)
def test_cases_small(m, n, l, t, correct_age):
    """ tests """
    age = elder_age(m, n, l, t)
    assert age == correct_age
