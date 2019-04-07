"""

Test suite 'Faberge easter eggs crush test [linear]' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test-linear

"""

import pytest
from solutions.farberge_easter_eggs_crush_test_linear import height

FIXED_TESTS = [(1, 51, 51),
               (2, 1, 1),
               (4, 17, 3213),
               (16, 19, 524096),
               (23, 19, 524287),
               (13, 550, 621773656),
               (531, 550, 424414512),
               (10 ** 4, 10 ** 5, 132362171),
               (8*10 ** 4, 10 ** 5, 805097588),
               (3000, 2 ** 200, 141903106),
               (8*10 ** 4, 4*10 ** 4, 616494770),
               (4*10 ** 4, 8*10 ** 4, 303227698)
              ]

@pytest.mark.parametrize('eggs, tries, floor', FIXED_TESTS)
def test_fixed(eggs, tries, floor):
    """ tests """
    assert height(eggs, tries) == floor
