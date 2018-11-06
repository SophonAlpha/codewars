"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""
import numpy as np

def elder_age(m, n, l, t):
    m, n = (n, m) if n > m else (m, n)
    donate_time = 0
    level = largest_sqare_tile(m)
    m1 = 8**level if level > 0 else m
    n1 = m1 if n > m1 else n
    donate_time += tile_time(m1, n1, l, t, 0, 0, level)
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
        quo, rem = divmod(n, sub_m)
        sub_n = sub_m
        origin = tile_time(sub_m, sub_n, l, t, origin, 0, level - 1)
    quo, rem = divmod(m, 8**(level + 1))
    if quo == 0 and level == 0:
        time = tile(0, m, 0, n, l, t)
    elif quo == 0 and level > 0:
        pass
    else:
        time = m * ((start_col + start_col + m - 1) / 2) * n
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
    m, n, l, t = 16, 8, 0, 100000
    print(elder_age(m, n, l, t))
    print(tile(m, n, l, t**2))