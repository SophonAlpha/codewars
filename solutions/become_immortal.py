"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""
import numpy as np

def elder_age(m, n, l, t):
    xor_time = 0
    index = 0
    while m > 0:
        m, n = (n, m) if n > m else (m, n) # ensure m always contains the bigger of two dimensions 
        level = largest_sqare_tile(m) 
        sub_m = 8**level
        quo, rem = divmod(n, sub_m)
        sub_n = 8 if quo > 0 else rem
        xor_time += tile_time(sub_m, sub_n, l, t, 0, index, level - 1)
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
        quo, rem = divmod(n, sub_m)
        sub_n = 8 if quo > 0 else rem
        origin = tile_time(sub_m, sub_n, l, t, origin, 0, level - 1)
    tile_width = 8**level
    column = start_col
    columns = np.arange(start_col, start_col + m, tile_width)
    
    # TODO; fix tile_width multiplicator for 8x8 tile
    col_adder = np.multiply(columns, tile_width*tile_width)
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
    m, n, l, t = 64, 67, 0, 100000
    print(elder_age(m, n, l, t))
    print(tile(m, n, l, t**2))