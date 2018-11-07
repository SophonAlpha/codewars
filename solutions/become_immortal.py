"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""
import numpy as np

VALUES = np.array([[0, 1, 2, 3, 4, 5, 6, 7],
                   [1, 0, 3, 2, 5, 4, 7, 6],
                   [2, 3, 0, 1, 6, 7, 4, 5],
                   [3, 2, 1, 0, 7, 6, 5, 4],
                   [4, 5, 6, 7, 0, 1, 2, 3],
                   [5, 4, 7, 6, 1, 0, 3, 2],
                   [6, 7, 4, 5, 2, 3, 0, 1],
                   [7, 6, 5, 4, 3, 2, 1, 0]])

def elder_age(m, n, l, t):
    donate_time = 0
    m_start, n_start = 0, 0
    m_end, n_end = m, n
    for section in range(0, 4):
        dm = m_end - m_start
        dn = n_end - n_start
        if dn > dm:
            m_start, m_end, n_start, n_end = n_start, n_end, m_start, m_end
            dm, dn = dn, dm
        m_level = largest_sqare_tile(m_end - m_start)
        n_level = largest_sqare_tile(n_end - n_start)
        m_start, n_start = 0, 0
        m_end = m_start + divmod(dm, 8**m_level)[0] * 8**m_level
        n_end = n_start + divmod(dn, 8**n_level)[0] * 8**n_level
        donate_time += tile_time(m_start, m_end, n_start, n_end, 0, m_level, l, t)



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

def tile_time(m_start, m_end, n_start, n_end, origin, level, l, t):
    
    m = m_end
    n = n_end
    
    if level > 0:
        sub_m = 8**level
        sub_n = sub_m if n > sub_m else n
        origin = tile_time(None, sub_m, None, sub_n, origin, level - 1, l, t)
    index = np.arange(0, 8**(level + 1), 8**level)
    if level == 0:
        xor_arr = np.add(np.multiply(index, 8**level * 8**level), origin)
    else:
        square_size = 8**(level - 1)
        m_quo = divmod(m, square_size)[0] if m < 8**level else 8**level
        n_quo = divmod(n, square_size)[0] if n < 8**level else 8**level
        xor_arr = np.add(np.multiply(index, m_quo * square_size * n_quo * square_size), origin)
    val_col = 1 if m < 8**level else divmod(m, 8**level)[0]
    val_row = 1 if n < 8**level else divmod(n, 8**level)[0]
    time = np.sum(xor_arr[VALUES[:val_row, :val_col]])
    return time

def tile(m_s, m_e, n_s, n_e, l, t):
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e), np.arange(m_s, m_e))).reshape(2, -1)
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    donate_time = np.sum(trans_loss) % t
    return donate_time


if __name__ == "__main__":
    m, n, l, t = 545, 435, 342, 1000007
    m, n, l, t = 28827050410, 35165045587, 7109602, 13719506
    m, n, l, t = 545, 435, 342, 1000007
    m, n, l, t = 64, 64, 0, 100000
    m, n, l, t = 1024, 512, 0, 100000
    m, n, l, t = 67, 67, 0, 100000
    m, n, l, t = 5, 6, 0, 100000
    m, n, l, t = 5, 16, 0, 100000
    m, n, l, t = 19, 53, 0, 100000
    m, n, l, t = 19, 58, 0, 100000
    print(elder_age(m, n, l, t))
    print(tile(m, n, l, t**2))