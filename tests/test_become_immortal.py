"""

Test suite Become Immortal kata:
https://www.codewars.com/kata/become-immortal

"""

import pytest
import random
from solutions.become_immortal import elder_age
from solutions.become_immortal import loss_array

"""
100 test cases
m,n: 2^5 - 2^10
l: 0 - 19
t: 2^5 - 2^15

300 test cases
m,n: 2^8 - 2^20
l: 0 - 9999
t: 2^10 - 2^20

500 test cases
m,n: 2^32 - 2^64
l: 0 - 9999999
t: 2^16 - 2^32
"""

def generate_100_test_cases():
    """
    100 test cases
    m,n: 2^5 - 2^10
    l: 0 - 19
    t: 2^5 - 2^15
    """
    tests = []
    for _ in range(0,100):
        m = random.randint(2**5, 2**10)
        n = random.randint(2**5, 2**10)
        l = random.randint(0, 19)
        t = random.randint(2**5, 2**15)
        tests.append(tests)
    return tests

TESTS = [(8, 5, 1, 100, 5),
         (7, 4, 1, 100, 66),
         (8, 8, 0, 100007, 224),
         (25, 31, 0, 100007, 11925),
         (5, 45, 3, 1000007, 4323),
         (31, 39, 7, 2345, 1586),
         (545, 435, 342, 1000007, 808451),
         (28827050410, 35165045587, 7109602, 13719506, 5456283),
         (706, 120, 12, 6983, 1525),
         (176, 110, 20, 2805, 767),
         (68, 444, 1, 4091, 3932),
         (89, 137, 2, 53, 47),
         (331, 49, 5, 225, 121),
         (113, 598, 5, 148, 104),
         (965, 807, 13, 2572, 5),
         (594, 235, 15, 881, 613),
         (168, 78, 15, 2783, 2661),
         (76, 809, 17, 1871, 1382),
         (76, 64, 14, 19488, 4576),
         (200, 318, 16, 76, 48),
         (60, 456, 20, 784, 312),
         (251, 524, 8, 25695, 24385),
         (805, 117, 10, 53, 24),
         (593, 440, 5, 2743, 2398),
         (204, 60, 15, 23206, 15956),
         (610, 354, 15, 1210, 356),
         (71, 983, 2, 39, 22),
         (107, 982, 7, 574, 297),
         (57, 59, 15, 129, 6),
         (868, 702, 1, 2610, 1478),
         (314, 67, 3, 540, 131),
         (149, 111, 11, 40, 28),
         (338, 975, 6, 90, 29),
         (72, 654, 1, 956, 604),
         (96, 343, 14, 709, 293),
         (321, 77, 17, 60, 42),
         (64, 212, 18, 2089, 61),
         (47, 41, 9, 26369, 11463),
         (880, 108, 13, 2909, 75),
         (81, 414, 20, 15690, 13567),
         (66, 304, 4, 122, 112),
         (119, 359, 9, 18148, 5250),
         (140, 190, 0, 1619, 121),
         (993, 65, 9, 162, 130),
         (73, 65, 19, 6400, 3520),
         (85, 605, 1, 2212, 2104),
         (291, 138, 15, 26607, 9287),
         (877, 915, 20, 76, 27),
         (211, 463, 0, 95, 45),
         (139, 951, 12, 24426, 20772),
         (78, 59, 3, 451, 437)]

@pytest.mark.parametrize('m, n, l, t, correct_age', TESTS)
def test_cases_small(m, n, l, t, correct_age):
    """ tests """
    total_time, donate_time = elder_age(m, n, l, t)
    assert donate_time == correct_age

@pytest.mark.parametrize('m, n, l, t, correct_age', TESTS)
def test_with_naive_calculation(m, n, l, t, correct_age):
    """ tests """
    total_time, donate_time = elder_age(m, n, l, t)
    naive_age = loss_array(0, m, 0, n, l, t)[0]
    assert total_time == naive_age
