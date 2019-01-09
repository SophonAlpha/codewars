"""
My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

performance statistics for
m = 28827050410, n = 35165045587, l = 7109602, t = 13719506, age = 5456283

    baseline:                                  'elder_age', 0.14357590786395225 s
    optimised tile_time() function:            'elder_age', 0.09438958444985779 s
    optimised with sum of arithmetic sequence: 'elder_age', 0.05584444502951191 s
    new tile_generator(), sub tile at 8**x:    'elder_age', 0.00657040719656825 s
"""
import numpy as np
np.seterr(over='raise')
from solutions.performance import Profile

from collections import deque

PERFORMANCE_STATS = []

@Profile(stats=PERFORMANCE_STATS)
def elder_age(m, n, l, t):
    donate_time = 0
    for m_start, dm, n_start, dn in tile_generator(m, n):
        donate_time += tile_time(m_start, dm, n_start, dn, l)
    donate_time = donate_time % t
    return donate_time

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
            tile = (m_start + sub_m, (m_start + m) - (m_start + sub_m),
                    n_start + sub_n, (n_start + n) - (n_start + sub_n))
            if not tile in queue: queue.append(tile) 
        # upper right sub tile
        if m_start + sub_m < m_start + m:
            tile = (m_start + sub_m, (m_start + m) - (m_start + sub_m),
                    n_start, sub_n)
            if not tile in queue: queue.append(tile)
        # lower left sub tile
        if n_start + sub_n < n_start + n:
            tile = (m_start, sub_m,
                    n_start + sub_n, (n_start + n) - (n_start + sub_n))
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
    return int((n * (a_1 + a_n)) / 2)

# @Profile(stats=PERFORMANCE_STATS)
def small_tile_sum(m_start, m, n_start, n, l):
    rows, cols = np.array(np.meshgrid(np.arange(n_start, n_start + n, dtype=object),
                                      np.arange(m_start, m_start + m, dtype=object)))
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    tile_sum = np.sum(trans_loss)
    return tile_sum

def xor_sum(m_s, m_e, n_s, n_e, l, t):
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e, dtype=object),
                                      np.arange(m_s, m_e, dtype=object)))
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    loss = np.subtract(np.sum(xor_arr), np.sum(trans_loss))
    donate_time = np.sum(trans_loss) % t
    return np.sum(xor_arr), loss, donate_time

if __name__ == "__main__":
    print(elder_age(28827050410, 35165045587, 7109602, 13719506)) # 5456283
    print(PERFORMANCE_STATS)
