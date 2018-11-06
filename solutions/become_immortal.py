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
    m, n = (n, m) if n > m else (m, n)
    donate_time = 0
    level = largest_sqare_tile(m)
    m1 = m if m < 8**level else divmod(m, 8**level)[0] * 8**level
    n1 = n if n < 8**level else divmod(n, 8**level)[0] * 8**level
    donate_time += tile_time(m1, n1, l, t, 0, 0, level)

    """
	level 0:
		origin = 0
		(0, 0) = origin
		(0, column) = column * 8**level * 8**level + (0, 0)

	level 1 (8):
		origin = (8x8 sum of level 0)
		(0, column) = column * 8**level * 8**level + (0, 0)

	"""

    return donate_time

def xor_time_sum(m_s, m_e, n_s, n_e):
    return (m_e - m_s) * ((m_s + m_e - 1) / 2) * (n_e - n_s)

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

def tile_time(m, n, l, t, origin, start_col, level):
    if level > 0:
        sub_m = 8**level
        sub_n = sub_m if n > sub_m else n
        origin = tile_time(sub_m, sub_n, l, t, origin, 0, level - 1)
    index = np.arange(0, 8**(level + 1), 8**level)
    if level == 0:
        xor_arr = np.add(np.multiply(index, 8**level * 8**level), origin)
    else:
        square_size = 8**(level - 1)
        m_quo, _ = divmod(m, square_size)
        n_quo, _ = divmod(n, square_size)
        xor_arr = np.add(np.multiply(index, m_quo * square_size * n_quo * square_size), origin)
    val_row = 1 if m < 8**level else divmod(m, 8**level)[0]
    val_col = 1 if n < 8**level else divmod(n, 8**level)[0]
    time = np.sum(xor_arr[VALUES[:val_row, :val_col]])
    
#     m_count = m if level == 0 else 8**(level - 1)
#     n_count = n if level == 0 else 8**(level - 1)
#     quo, rem = divmod(m, 8**(level + 1))
#     if quo == 0 and level == 0:
#         time = tile(0, m, 0, n, l, t)
#     elif quo == 0 and level > 0:
#         pass
#     else:
#         time = m * ((start_col + start_col + m - 1) / 2) * n
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
    m, n, l, t = 19, 53, 0, 100000
    m, n, l, t = 5, 6, 0, 100000
    m, n, l, t = 5, 16, 0, 100000
    print(elder_age(m, n, l, t))
    print(tile(m, n, l, t**2))