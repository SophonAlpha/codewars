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
    donate_time1 = tile(m, n, l, t)
    exp = 0
    while True:
        fit, _ = divmod(m, 8**exp)
        if fit == 1:
            break
        exp += 1
    level = exp - 1
    m_start = 8**(level + 1)
    n_start = 8**(level + 1)
    donate_time2 = tile2(m_start, n_start, l, t, 0, 0, level)
    return donate_time2

    """
    m = 35,165,045,587
    q =  3,603,381,301
    """

def tile2(m, n, l, t, origin, start_col, level):
    if level > 0:
        m_start = 8**level
        n_start = 8**level
        origin = tile2(m_start, n_start, l, t, origin, start_col, level - 1)
    tile_width = 8**level
    column = start_col
    columns = np.arange(start_col, start_col + m, tile_width)
    col_adder = np.multiply(columns, tile_width**2)
    col_adder = np.add(col_adder, origin)
    tile_time = np.sum(col_adder) * 8

#     t = 0
#     # the sum of xors of tile originating at relative position 0, 0
# #     xor_sum = np.sum(origin)
#     while column < start_col + m:
#         # adder that represents the sum to be added for tiles along columns
#         # ' * 8'     - tile width in cells by which to shift to the right
#         # ' * 8 * 8' - number of cells in the tile
#         col_adder = column * tile_width * tile_width
#         t = t + origin + col_adder
#         column += tile_width
#     tile_time = t * 8 # multiplied by number of tile rows

#         tile_time = (224 + \
#                      column * 8 * 8 * 8 - \
#                      l * 64 + \
#                      4 * l * (l + 1)) % t
    return tile_time


def tile(m, n, l, t):
    rows, cols = np.array(np.meshgrid(np.arange(n), np.arange(m))).reshape(2, -1)
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    donate_time = np.sum(trans_loss) % t
    return donate_time


if __name__ == "__main__":
    m, n, l, t = 545, 435, 342, 1000007
    m, n, l, t = 28827050410, 35165045587, 7109602, 13719506
    m, n, l, t = 545, 435, 342, 1000007
    m, n, l, t = 8, 8, 0, 100000
    m, n, l, t = 64, 64, 0, 100000
    m, n, l, t = 512, 512, 0, 100000
    print(elder_age(m, n, l, t))
    print(tile(m, n, l, t**2))