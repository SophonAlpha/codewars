"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""
import numpy as np


"""
m = 545, n = 435, l = 342, t = 1000007, age = 808451

    m = 35,165,045,587
    q =  3,603,381,301

"""

def elder_age(m, n, l, t):
    xor_time = 0
    index = 0
    while m > 0:
        m, n = (n, m) if n > m else (m, n) # ensure m always contains the bigger of two dimensions 
        exp = largest_sqare_tile(m) 
        level = exp - 1
        sub_m = 8**exp
        quo, rem = divmod(n, sub_m)
        sub_n = quo * 8 + rem
    #     n_start = 8**(level + 1)
        xor_time += tile_time(sub_m, sub_n, l, t, 0, index, level)
        m = m - sub_m
        index += sub_m
    return xor_time

def largest_sqare_tile(size):
    exp = 0
    while True:
        fit, _ = divmod(size, 8**exp)
        if fit == 1:
            break
        exp += 1
    return exp

def tile_time(m, n, l, t, origin, start_col, level):
    if level > 0:
        sub_m = 8**level
#         sub_n = 8**level
        quo, rem = divmod(n, sub_m)
        sub_n = quo * 8 + rem
        origin = tile_time(sub_m, sub_n, l, t, origin, start_col, level - 1)
    tile_width = 8**level
    column = start_col
    columns = np.arange(start_col, start_col + m, tile_width)
    col_adder = np.multiply(columns, tile_width**2)
    col_adder = np.add(col_adder, origin)
    time = np.sum(col_adder) * n

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
    return time


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
    m, n, l, t = 64, 64, 0, 100000
    m, n, l, t = 1024, 512, 0, 100000
    m, n, l, t = 64, 88, 0, 100000
    print(elder_age(m, n, l, t))
    print(tile(m, n, l, t**2))