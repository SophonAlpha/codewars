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

    """
    m = 35,165,045,587
    q =  3,603,381,301
    
    8**12 = 68,719,476,736
    
    tile_delta = np.array([[0, 1, 2, 3, 4, 5, 6, 7],
                           [1, 0, 3, 2, 5, 4, 7, 6],
                           [2, 3, 0, 1, 6, 7, 4, 5],
                           [3, 2, 1, 0, 7, 6, 5, 4],
                           [4, 5, 6, 7, 0, 1, 2, 3],
                           [5, 4, 7, 6, 1, 0, 3, 2],
                           [6, 7, 4, 5, 2, 3, 0, 1],
                           [7, 6, 5, 4, 3, 2, 1, 0]])

    """

def tile_group(m, n, l, t):
    q, r = divmod(max(m, n), 8)
    tile_index = 0
    while tile_index < q:
        tile_time = (224 + \
                     tile_index * 512 - \
                     l * 64 + \
                     4 * l * (l + 1)) % t
        print(tile_time)
        tile_index += 1
    return tile_time


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
    m, n, l, t = 64, 64, 0, 100000
    tile_group(m, n, l, t)