"""

Test suite Become Immortal kata:
https://www.codewars.com/kata/become-immortal

"""

import pytest
import random
from solutions.become_immortal import tile_generator
from solutions.become_immortal import elder_age
from solutions.become_immortal import xor_sum
from solutions.become_immortal import modulo

def generate_test_cases():
    """
    Automatic generation of test cases. We use the naive solution algorithm
    implemented in function xor_sum(m_s, m_e, n_s, n_e, l, t) to test the result
    of the performance optimised function elder_age(m, n, l, t).
    """
    tests = []
    for _ in range(0, 3000):
        m = random.randint(2**5, 8**4)
        n = random.randint(2**5, 8**4)
        l = random.randint(0, 300000)
        t = random.randint(2**5, 8**5)
        tests.append((m, n, l, t))
    return tests

def generate_modulo_test_cases():
    tests = []
    for _ in range(0, 1000):
        m = random.randint(2**32, 2**128)
        t = random.randint(2**16, 2**32)
        tests.append((m, t))
    return tests

FIXED_TESTS = [(8, 5, 1, 100, 5),
               (7, 4, 1, 100, 66),
               (8, 8, 0, 100007, 224),
               (25, 31, 0, 100007, 11925),
               (5, 45, 3, 1000007, 4323),
               (31, 39, 7, 2345, 1586),
               (310, 38, 159, 14107, 12604),
               (931, 708, 235, 12518, 3898),
               (177, 660, 462, 14783, 10656),
               (665, 491, 459, 3053, 312),
               (639, 282, 833, 20949, 7593),
               (146, 186, 21, 7662, 6628),
               (545, 435, 342, 1000007, 808451),
               (328, 334, 12, 27974, 13932),
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

LARGE_TESTS = [(28827050410, 35165045587, 7109602, 13719506, 5456283),
               (14894658662517258, 2079750097359417088, 5876922, 6920851, 5331202),
               (145858900537694688, 9909527706292780, 8654247, 363101, 324438)]

@pytest.mark.parametrize('m, n, l, t, correct_age', FIXED_TESTS)
def test_tile_generator_fixed(m, n, l, t, correct_age):
    """ tests """
    array_size = sum([dm * dn for _, dm, _, dn in tile_generator(m, n)])
    assert array_size == m * n

@pytest.mark.parametrize('m, n, l, t, correct_age', LARGE_TESTS)
def test_tile_generator_large_fixed(m, n, l, t, correct_age):
    """ tests """
    array_size = sum([dm * dn for _, dm, _, dn in tile_generator(m, n)])
    assert array_size == m * n

@pytest.mark.parametrize('m, n, l, t, correct_age', FIXED_TESTS)
def test_fixed(m, n, l, t, correct_age):
    """ tests """
    donate_time = elder_age(m, n, l, t)
    assert donate_time == correct_age

@pytest.mark.parametrize('m, n, l, t, correct_age', LARGE_TESTS)
def test_large_fixed(m, n, l, t, correct_age):
    """ tests """
    donate_time = elder_age(m, n, l, t)
    assert donate_time == correct_age

@pytest.mark.parametrize('m, n, l, t', generate_test_cases())
def test_random_tests(m, n, l, t):
    """ tests """
    donate_time = elder_age(m, n, l, t)
    _, _, naive_donate_time = xor_sum(0, m, 0, n, l, t)
    assert donate_time == naive_donate_time

@pytest.mark.parametrize('m, t', generate_modulo_test_cases())
def test_modulo(m, t):
    """ tests """
    donate_time = modulo(m, t)
    assert donate_time == m % t
