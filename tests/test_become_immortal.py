"""

Test suite Become Immortal kata:
https://www.codewars.com/kata/become-immortal

"""

import pytest

from solutions.become_immortal import elder_age

TESTS = [(8, 5, 1, 100, 5)]

@pytest.mark.parametrize('m, n, l, t, correct_age', TESTS)
def test_cases(m, n, l, t, correct_age):
    """ tests """
    age = elder_age(m, n, l, t)
    assert age == correct_age
