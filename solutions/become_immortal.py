"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""
import numpy as np


"""
m = 545, n = 435, l = 342, t = 1000007, age = 808451
"""

def elder_age(m, n, l, t):
    donate_time = tile(m, n, l, t)
    return donate_time

def tile_group(m, n, l, t):
    q, r = divmod(max(m, n), 8)
    m_starts = np.append(np.arange(0, q * 8, 8), q * 8)
    m_ends = np.append(np.arange(7, q * 8, 8), q * 8 + r)
    params = np.column_stack((m_starts, m_ends,
                              np.repeat(0, m_starts.shape[0]),
                              np.repeat(7, m_starts.shape[0]),
                              np.repeat(l, m_starts.shape[0]),
                              np.repeat(t, m_starts.shape[0])))

    """
    m = 35,165,045,587
    q =  3,603,381,301
    """

    tile_index = 0
    while tile_index <= q:
        m_starts = tile_index * 8
        m_ends = m_starts + 7
        tile_time = tile(m_starts, m_ends, l, t)
        tile_index += 1


        
    

def tile(m_s, m_e, l, t):
    n_s, n_e = 0, 7
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e),
                                      np.arange(m_s, m_e))).reshape(2, -1)
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    donate_time = np.sum(trans_loss) % t
    return donate_time


if __name__ == "__main__":
    m, n, l, t = 545, 435, 342, 1000007
    m, n, l, t = 28827050410, 35165045587, 7109602, 13719506
    tile_group(m, n, l, t)