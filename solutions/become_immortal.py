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
        donate_time += tile_time(m_start, dm, n_start, dn, origin, level)
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
    if level > 0:
        sub_dm = min(dm, 8**level)
        sub_dn = min(dn, 8**level)
        origin = np.int64(tile_time(m_start, sub_dm, n_start, sub_dn,
                                    origin, level - 1))
        if level > 1 and sub_dn != sub_dm:
            return origin
    seg_start = divmod(m_start, 8**(level + 1))[0] * 8**(level + 1)
    index = np.arange(seg_start, seg_start + 8**(level + 1), 8**level,
                      dtype=np.int64)
    index = np.bitwise_xor(index, n_start)

    val_col = 1 if dm < 8**level else divmod(dm, 8**level)[0]
    val_row = 1 if dn < 8**level else divmod(dn, 8**level)[0]
    if level == 0:
        xor_arr = np.multiply(np.arange(0, 8), 8**level * 8**level)
        if dm < 8 and dn < 8:
            xor_arr = index
    else:
        square_size = 8**(level - 1)
        m_quo = divmod(dm, square_size)[0] if dm < 8**level else 8**level
        n_quo = divmod(dn, square_size)[0] if dn < 8**level else 8**level
        xor_arr = np.add(np.multiply(index, m_quo * square_size * n_quo * square_size), 
                         origin)
    xor_arr = xor_arr[VALUE_MAP[:val_row, :val_col]]
    time = np.sum(xor_arr)
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
    m, n, l, t = 545, 435, 342, 1000007
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
    m, n, l, t = 545, 435, 342, 1000007
    print(elder_age(m, n, l, t))
    print(tile(m, n, l, t**2))