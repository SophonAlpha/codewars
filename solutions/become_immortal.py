"""
My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

performance statistics for
m = 28827050410, n = 35165045587, l = 7109602, t = 13719506, age = 5456283

    baseline:                                  'elder_age', 0.14358 s
    optimised tile_time() function:            'elder_age', 0.09439 s
    optimised with sum of arithmetic sequence: 'elder_age', 0.05584 s
    new tile_generator(), sub tile at 8**x:    'elder_age', 0.00657 s
    small_tile_sum() as list comprehension:    'elder_age', 0.00208 s
"""

from solutions.performance import Profile
import numpy as np
np.seterr(over='raise')
from collections import deque

PERFORMANCE_STATS = []

@Profile(stats=PERFORMANCE_STATS)
def elder_age(m, n, l, t):
    donate_time = 0
    for m_start, dm, n_start, dn in tile_generator(m, n):
        donate_time = (donate_time % t + tile_time(m_start, dm, n_start, dn, l) % t) % t
    return donate_time

def test_tile_generator(m, n):
    for m_start, dm, n_start, dn in tile_generator(m, n):
        print(m_start, dm, n_start, dn)

# @Profile(stats=PERFORMANCE_STATS)
def tile_generator(m, n):
    queue = deque()
    m_start, n_start = 0, 0
    queue.append((m_start, m, n_start, n))
    while True:
        try:
            m_start, m, n_start, n = queue.pop()
        except IndexError:
            break
        # upper left sub tile
        m_level, n_level = largest_sqare_tile(m), largest_sqare_tile(n)
        if m_level >= n_level and m_level > 0:
            sub_m = 8**m_level
            sub_n = min(n, 8**m_level)
        elif m_level < n_level:
            sub_m = min(m, 8**n_level)
            sub_n = 8**n_level
        else:
            sub_m = m
            sub_n = n
        yield m_start, sub_m, n_start, sub_n
        # lower right sub tile
        if m_start + sub_m < m_start + m and n_start + sub_n < n_start + n:
            tile = (m_start + sub_m, m - sub_m,
                    n_start + sub_n, n - sub_n)
            if not tile in queue: queue.append(tile)
        # upper right sub tile
        if m_start + sub_m < m_start + m:
            tile = (m_start + sub_m, m - sub_m,
                    n_start, sub_n)
            if not tile in queue: queue.append(tile)
        # lower left sub tile
        if n_start + sub_n < n_start + n:
            tile = (m_start, sub_m,
                    n_start + sub_n, n - sub_n)
            if not tile in queue: queue.append(tile)

# @Profile(stats=PERFORMANCE_STATS)
def largest_sqare_tile(size):
    exp = 1
    if size < 8**exp:
        return 0
    while True:
        fit, _ = divmod(size, 8**(exp + 1))
        if fit == 0:
            break
        exp += 1
    return exp

# @Profile(stats=PERFORMANCE_STATS)
def tile_time(m_start, dm, n_start, dn, l):
    if dm < 1 or dn < 1:
        return 0
    m_start, dm, n_start, dn = swap_width_height(m_start, dm, n_start, dn)
    if dm < 8:
        tile_sum = small_tile_sum(m_start, dm, n_start, dn, l)
    else:
        seq_start = m_start ^ n_start
        seq_end = (m_start + dm - 1) ^ n_start
#         check_consecutiveness(seq_start, seq_end, dm)
        if seq_end <= l:
            tile_sum = 0
        elif seq_start <= l < seq_end:
            tile_sum = sum_seq(seq_start, seq_end) * dn
            loss = (sum_seq(seq_start, l - 1) + (seq_end - (l - 1)) * l) * dn
            tile_sum -= loss
        else:
            tile_sum = sum_seq(seq_start, seq_end) * dn
            loss = dm * l * dn
            tile_sum -= loss
    return tile_sum

# @Profile(stats=PERFORMANCE_STATS)
def swap_width_height(m_start, dm, n_start, dn):
    if dn > dm:
        m_start, dm, n_start, dn = n_start, dn, m_start, dm
    return m_start, dm, n_start, dn

# @Profile(stats=PERFORMANCE_STATS)
def sum_seq(a_1, a_n):
    """
    Calculate sum of arithmetic sequence.
    """
    n = a_n - a_1 + 1
    return (n * (a_1 + a_n)) // 2

# @Profile(stats=PERFORMANCE_STATS)
def small_tile_sum(m_start, m, n_start, n, l):
    tile_sum = sum([((row ^ col) - l) if (row ^ col) > l else 0
                    for row in range(n_start, n_start + n)
                    for col in range(m_start, m_start + m)])
    return tile_sum

def xor_sum(m_s, m_e, n_s, n_e, l, t):
    """
    Naive solution algorithm. Suitable only for small array sizes m, n < 3,000.
    """
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e, dtype=object),
                                      np.arange(m_s, m_e, dtype=object)))
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    loss = np.subtract(np.sum(xor_arr), np.sum(trans_loss))
    donate_time = np.sum(trans_loss) % t
    return np.sum(xor_arr), loss, donate_time

# TODO: remove this test function in final version
def check_consecutiveness(seq_start, seq_end, dm):
    level = largest_sqare_tile(dm)
    diff = seq_end - (seq_start - 1)
    if diff == dm and diff == 8**level:
        print('ok = {}, level: {}'.format(dm, level))
    else:
        print('failure = {}, level: {}'.format(dm, level))

# TODO: remove this test function in final version
def sub_sizes(size):
    while size > 0:
        level = largest_sqare_tile(size)
        sub_size = 8**level if level > 0 else size
        print(sub_size)
        size = size - sub_size

# TODO: remove this test function in final version
def modulo(long_int, mod_int):
    result = 0
    for pos in range(0, len(str(long_int))): 
        result = (result * 10 + int(str(long_int)[pos])) % mod_int    
    return result

if __name__ == "__main__":
#     test_tile_generator(14894658662517258, 2079750097359417088)
    print(elder_age(16, 8, 8, 100000)) # 224
    print(elder_age(14894658662517258, 2079750097359417088, 5876922, 6920851)) # 5331202
    print(elder_age(145858900537694688, 9909527706292780, 8654247, 363101)) # 324438
    print(PERFORMANCE_STATS)
