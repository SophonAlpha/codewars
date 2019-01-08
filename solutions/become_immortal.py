"""
My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

performance statistics:

    baseline:                                  'elder_age', 0.14357590786395225 s
    optimised tile_time() function:            'elder_age', 0.09438958444985779 s
    optimised with sum of arithmetic sequence: 'elder_age', 0.05584444502951191 s
"""
import numpy as np
np.seterr(over='raise')
from solutions.performance import Profile

from collections import deque

PERFORMANCE_STATS = []

@Profile(stats=PERFORMANCE_STATS)
def elder_age(m, n, l, t):
    total_time = 0
    total_loss = 0
    m, n = (m, n) if m > n else (n, m)
    m_start, n_start = 0, 0
    m_end, n_end = m, n
    while n_start != n_end:
        dm, dn = m_end - m_start, n_end - n_start
        m_level, n_level = largest_sqare_tile(dm), largest_sqare_tile(dn)
        dm = clamp(divmod(dm, 8**m_level)[0], 1, 8) * 8**m_level
        dn = clamp(divmod(dn, 8**n_level)[0], 1, 8) * 8**n_level
        level = max(m_level, n_level)
        time, _ = tile_time(m_start, dm, n_start, dn, level, l)
        loss = tile_loss(m_start, dm, n_start, dn, level, l)
        total_time += time
        total_loss += loss
        m_start = m_start + dm
        m_end = m
        if m_start == m_end:
            m_start, n_start = 0, n_start + dn
            m_end, n_end = m, n
    donate_time = total_time - total_loss
    donate_time = donate_time % t
    return total_time, donate_time

def tile_generator(m, n):
    queue = deque()
    m, n = (m, n) if m > n else (n, m)
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
        yield m_start, sub_m, n_start, sub_n
        # lower right sub tile
        if m_start + sub_m < m_start + m and n_start + sub_n < n_start + n:
            tile = (m_start + sub_m, m - (m_start + sub_m),
                    n_start + sub_n, n - (n_start + sub_n))
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
def tile_generator_v1(m, n):
    m, n = (m, n) if m > n else (n, m)
    m_start, n_start = 0, 0
    m_end, n_end = m, n
    while n_start != n_end:
        dm, dn = m_end - m_start, n_end - n_start
        m_level, n_level = largest_sqare_tile(dm), largest_sqare_tile(dn)
        dm = clamp(divmod(dm, 8**m_level)[0], 1, 8) * 8**m_level
        dn = clamp(divmod(dn, 8**n_level)[0], 1, 8) * 8**n_level
        yield m_start, dm, n_start, dn
        m_start = m_start + dm
        m_end = m
        if m_start == m_end:
            m_start, n_start = 0, n_start + dn
            m_end, n_end = m, n

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
def tile_time(m_start, dm, n_start, dn, level, l):
    if dm < 1 or dn < 1:
        return 0
    m_start, dm, n_start, dn = swap_width_height(m_start, dm, n_start, dn)
    # calculate the xor sum values and the boundaries
    if level == 0:
        m_values = range(m_start, m_start + 8)
    else:
        m_values = range(m_start, m_start + 8**(level + 1), 8**level)
    xor_arr = [value ^ n_start for value in m_values]
    positions = [(value - min(xor_arr)) // 8**level for value in xor_arr]
    # number of rows and columns for current tile size
    tile_rows = divmod(dn, 8**level)[0]
    tile_rows = tile_rows if tile_rows > 0 else 1
    tile_cols = divmod(dm, 8**level)[0]
    tile_cols = tile_cols if tile_cols > 0 else 1
    if level > 0:
        # calculate sum of next smaller tile
        sub_m_start = m_start + xor_arr.index(min(xor_arr)) * 8**level
        sub_dm = min(dm, 8**level)
        sub_dn = min(dn, 8**level)
        tile_start_row = (n_start // 8**level) * 8**level
        seq_start = sub_m_start ^ tile_start_row
        seq_end = (sub_m_start + sub_dm - 1) ^ tile_start_row
        if seq_end <= l:
            sub_tile_sum = 0
        else:
            sub_tile_sum = sum_seq(max(seq_start, l), seq_end) * sub_dn
    else:
        sub_tile_sum = m_start ^ n_start
    # calculate the sum for the other tiles based on the sub_tile_sum
    if dm >= 8**level:
        delta = (sum_seq(8**level, 8**level + 8**level - 1) - \
                 sum_seq(0, 8**level - 1)) * min(dn, 8**level)
        xor_arr = [(value * delta) + sub_tile_sum for value in positions]
        xor_arr = map_row_to_array(xor_arr, tile_rows, tile_cols)
        time = sum([sum(row) for row in xor_arr])
    else:
        time = sub_tile_sum
    return time, xor_arr

# @Profile(stats=PERFORMANCE_STATS)
def map_row_to_array(first_row, num_rows, num_cols):
    first_row_to_8x8_map = [[0, 1, 2, 3, 4, 5, 6, 7],
                            [1, 0, 3, 2, 5, 4, 7, 6],
                            [2, 3, 0, 1, 6, 7, 4, 5],
                            [3, 2, 1, 0, 7, 6, 5, 4],
                            [4, 5, 6, 7, 0, 1, 2, 3],
                            [5, 4, 7, 6, 1, 0, 3, 2],
                            [6, 7, 4, 5, 2, 3, 0, 1],
                            [7, 6, 5, 4, 3, 2, 1, 0]]
    array = []
    for row_index in range(0, num_rows):
        new_row = [first_row[first_row_to_8x8_map[row_index][col_index]] 
                   for col_index in range(0, num_cols)]
        array.append(new_row)
    return array

# @Profile(stats=PERFORMANCE_STATS)
def swap_width_height(m_start, dm, n_start, dn):
    if dn > dm:
        m_start, dm, n_start, dn = n_start, dn, m_start, dm
    return m_start, dm, n_start, dn

# @Profile(stats=PERFORMANCE_STATS)
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

# @Profile(stats=PERFORMANCE_STATS)
def tile_loss(m_start, dm, n_start, dn, level, l):
    # ensure width is always bigger than height
    m_start, dm, n_start, dn = swap_width_height(m_start, dm, n_start, dn)
    # calculate the xor sum values and the boundaries
    if level == 0:
        m_values = range(m_start, m_start + 8)
    else:
        m_values = range(m_start, m_start + 8**(level + 1), 8**level)
    xor_arr = [value ^ n_start for value in m_values]
    xor_arr_boundaries = [divmod(value, 8**level)[0] * 8**level
                          for value in xor_arr]
    # number of rows and columns for current tile size
    num_rows = divmod(dn, 8**level)[0]
    num_rows = num_rows if num_rows > 0 else 1
    num_cols = divmod(dm, 8**level)[0]
    num_cols = num_cols if num_cols > 0 else 1
    # calculate width and height for next smaller tile
    sub_dm = min(dm, 8**level)
    sub_dn = min(dn, 8**level)
    # lifetime lower than range
    if l < min(xor_arr_boundaries):
        loss = num_cols * min(dm, 8**level) * dn * l
    # lifetime threshold within range
    if min(xor_arr_boundaries) <= l < max(xor_arr_boundaries) + 8**level:
        index = 0
        for index, value in enumerate(xor_arr_boundaries):
            if value <= l <= value + 8**level - 1:
                sub_m_start = m_start + index * 8**level
                break
        if level > 0:
            sub_loss = tile_loss(sub_m_start, sub_dm, n_start, sub_dn,
                                 level - 1, l)
        else:
            sub_loss = xor_arr[index]
        # calculate the loss array
        _, sum_arr = tile_time(m_start, 8 * 8**level, n_start, sub_dn, level)
        tiles_some_loss_idxs = [xor_arr_boundaries.index(value)
                                for value in xor_arr_boundaries
                                if value >= l]
        tiles_all_loss_idxs = [xor_arr_boundaries.index(value)
                              for value in xor_arr_boundaries
                              if value + 8**level <= l]
        loss_arr = [0] * 8
        for idx in tiles_all_loss_idxs:
            loss_arr[idx] = sum_arr[0][idx]
        loss_arr[index] = sub_loss
        for idx in tiles_some_loss_idxs:
            loss_arr[idx] = (8**level) * sub_dn * l
        loss_arr = map_row_to_array(loss_arr, num_rows, num_cols)
        loss = sum([sum(row) for row in loss_arr])
    # lifetime threshold larger than range
    if max(xor_arr_boundaries) + 8**level <= l:
        loss, _ = tile_time(m_start, dm, n_start, dn, level)
    return loss

def xor_arr_sum(m, n):
    sum = sum_seq(0, m - 1) * n
    return sum

def test_xor_arr_sum(m, n):
    return sum([sum([col ^ row for col in range(0, m)]) for row in range(0, n)])

# @Profile(stats=PERFORMANCE_STATS)
def sum_seq(a_1, a_n):
    """
    Calculate sum of arithmetic sequence.
    """
    n = a_n - a_1 + 1
    return int((n * (a_1 + a_n)) / 2)

def loss_array(m_s, m_e, n_s, n_e, l, t):
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e, dtype=object),
                                      np.arange(m_s, m_e, dtype=object)))
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    loss = np.subtract(np.sum(xor_arr), np.sum(trans_loss))
    donate_time = np.sum(trans_loss) % t
    return np.sum(xor_arr), loss, donate_time

if __name__ == "__main__":
    for tile in tile_generator(545, 435):
        print(tile)
#     print(elder_age(545, 435, 342, 1000007)) # 808451
#     print(elder_age(14894658662517258, 2079750097359417088, 5876922, 6920851)) # 5331202
#    print(PERFORMANCE_STATS)
