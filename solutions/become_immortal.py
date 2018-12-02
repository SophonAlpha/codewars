"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""
import numpy as np

VALUE_MAP = np.array([[0, 1, 2, 3, 4, 5, 6, 7],
                      [1, 0, 3, 2, 5, 4, 7, 6],
                      [2, 3, 0, 1, 6, 7, 4, 5],
                      [3, 2, 1, 0, 7, 6, 5, 4],
                      [4, 5, 6, 7, 0, 1, 2, 3],
                      [5, 4, 7, 6, 1, 0, 3, 2],
                      [6, 7, 4, 5, 2, 3, 0, 1],
                      [7, 6, 5, 4, 3, 2, 1, 0]])

def elder_age(m, n, l, t):
    donate_time = 0
    m, n = (m, n) if m > n else (n, m)
    m_start, n_start = 0, 0
    m_end, n_end = m, n
    while n_start != n_end:
        dm = m_end - m_start
        dn = n_end - n_start
        m_level = largest_sqare_tile(dm)
        n_level = largest_sqare_tile(dn)
        dm = divmod(dm, 8**m_level)[0] * 8**m_level
        dn = divmod(dn, 8**n_level)[0] * 8**n_level
        origin = np.int64(m_start ^ n_start)
        level = max(m_level, n_level)
        time = tile_time(m_start, dm, n_start, dn, origin, level)
        # TODO: remove debug check
#         time_check = time == xor_sum(m_start, m_start + dm, n_start, n_start + dn)
        # --------------------------
        donate_time += time
        m_start = m_start + dm
        m_end = m
        if m_start == m_end:
            m_start, n_start = 0, n_start + dn
            m_end, n_end = m, n
    max_l = min(l, max(m, n))
    total_loss = ((max_l**2 + max_l)/2 + (max(m, n) - 1 - max_l) * max_l) * min(m, n)
    donate_time = donate_time - total_loss
    donate_time = donate_time % t
    return donate_time

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

def tile_time(m_start, dm, n_start, dn, origin, level):
    if dn > dm:
        m_start, dm, n_start, dn = n_start, dn, m_start, dm
    index = np.bitwise_xor(np.arange(m_start, m_start + 8**(level + 1), 8**level), n_start)
    if level > 0:
        sub_m_start = m_start + index.argmin() * 8**level
        origin = sum_origin_tile(dm, dn, sub_m_start, n_start, 0, level)
    else:
        origin = np.bitwise_xor(m_start, n_start)
    if dm > 8**level:
        positions = np.int64(np.divide(np.subtract(index, index.min()), 8**level))
        rows = min(dn, 8**level)
        delta = np.sum(np.arange(8**level, 8**level + 8**level)) * rows - np.sum(np.arange(0, 8**level)) * rows
        xor_arr = np.add(np.multiply(positions, delta), origin)
        val_col = divmod(dm, 8**level)[0]
        val_row = max(1, divmod(dn, 8**level)[0])
        xor_arr = xor_arr[VALUE_MAP[:val_row, :val_col]]
        time = np.sum(xor_arr)
    else:
        time = origin
    return time

def sum_origin_tile(dm, dn, m_start, n_start, origin, level):
    if level > 1:
        index = np.bitwise_xor(np.arange(m_start, m_start + 8**level, 8**(level - 1), 
                                         dtype=np.int64), n_start)
        sub_dm = min(dm, 8**level)
        sub_dn = min(dn, 8**level)
        sub_m_start = m_start + index.argmin() * 8**(level - 1)
        origin = np.int64(sum_origin_tile(sub_dm, sub_dn, sub_m_start,
                                          n_start, origin, level - 1))
        positions = np.int64(np.divide(np.subtract(index, index.min()), 8**(level - 1)))
    else:
        index = np.bitwise_xor(np.arange(m_start, m_start + 8, dtype=np.int64), n_start)
    # TODO: find a better solution for sub indexing the index array
    if dn > 8:
        if divmod(dn, 8**(level - 1))[0] == 0:
            tile_rows = 1
        else:
            tile_rows = min(8, divmod(dn, 8**(level - 1))[0])
        cell_rows = min(dn, 8**(level - 1))
    else:
        tile_rows = max(1, divmod(dn, 8**(level - 1))[0])
        cell_rows = dn
    if level > 1:
        delta = np.sum(np.arange(8**(level - 1), 8**(level - 1) + 8**(level - 1))) * cell_rows - np.sum(np.arange(0, 8**(level - 1))) * cell_rows
        index = np.add(np.multiply(positions, delta), origin)
    time = np.sum(index) * tile_rows
    return time

def tile(m_s, m_e, n_s, n_e, l, t):
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e, dtype=np.int64),
                                      np.arange(m_s, m_e, dtype=np.int64))).reshape(2, -1)
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    donate_time = np.sum(trans_loss) % t
    return donate_time

def xor_sum(m_s, m_e, n_s, n_e):
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e, dtype=np.int64), np.arange(m_s, m_e, dtype=np.int64)))
    xor_arr = np.bitwise_xor(rows, cols)
    sum = np.sum(xor_arr)
    return sum

if __name__ == "__main__":
    m, n, l, t = 28827050410, 35165045587, 7109602, 13719506
    m, n, l, t = 64, 64, 0, 100000
    m, n, l, t = 1024, 512, 0, 100000
    m, n, l, t = 67, 67, 0, 100000
    m, n, l, t = 5, 6, 0, 100000
    m, n, l, t = 5, 16, 0, 100000
    m, n, l, t = 19, 53, 0, 100000
    m, n, l, t = 19, 58, 0, 100000
    m, n, l, t = 20, 91, 0, 100000
    m, n, l, t = 8, 5, 10, 100
    m, n, l, t = 20, 65, 0, 100000
    check_sum = xor_sum(0, 513, 0, 8)
    m, n, l, t = 513, 8, 0, 1000007
    m, n, l, t = 64, 8, 0, 1000007
    m, n, l, t = 72, 72, 0, 1000007
    m, n, l, t = 25, 31, 0, 100007
    m, n, l, t = 512, 513, 342, 1000007
    m, n, l, t = 7, 4, 1, 100
    m, n, l, t = 25, 31, 0, 100007
    m, n, l, t = 5, 45, 3, 1000007
    m, n, l, t = 31, 39, 7, 2345
    m, n, l, t = 545, 435, 342, 1000007
    m, n, l, t = 28827050410, 35165045587, 7109602, 13719506
    print(elder_age(m, n, l, t))
    print(tile(m, n, l, t**2))