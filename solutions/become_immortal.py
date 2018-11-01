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
    
    base_tile = np.array([[0, 1, 2, 3, 4, 5, 6, 7],
                          [1, 0, 3, 2, 5, 4, 7, 6],
                          [2, 3, 0, 1, 6, 7, 4, 5],
                          [3, 2, 1, 0, 7, 6, 5, 4],
                          [4, 5, 6, 7, 0, 1, 2, 3],
                          [5, 4, 7, 6, 1, 0, 3, 2],
                          [6, 7, 4, 5, 2, 3, 0, 1],
                          [7, 6, 5, 4, 3, 2, 1, 0]])
    
    8**1 x 8**1 =  8 x  8 cells =
    8x8 = origin_tile = base_tile
    
    8**2 x 8**2 = 64 x 64 cells =
    tile_index = 0 - 7
    t[tile_index] = (sum(origin_tile) + \        the sum of xors of base tile originating at 0, 0
                     tile_index * 8 * 8 * 8 - \  adder that represents the sum to be added for tiles along columns
                                                ' * 8'     - tile width by which to shift to the right
                                                ' * 8 * 8' - sum for tile with given dimensions where each cell 
                                                             value is equal to the tile width
                                                             
                                                 
                     l * 8 * 8 + \               the amount of loss for the whole tile
                     4 * l * (l + 1)) \          the sum of all values < 0 in a tile
                     % t                         max age
    tile_time = t[0] * 8 + \
                t[1] * 8 + \
                t[2] * 4 + \
                t[3] * 8 + \
                t[4] * 8 + \
                t[5] * 8 + \
                t[6] * 4 + \
                t[7] * 8
    """


origin_tile = np.array([[0, 1, 2, 3, 4, 5, 6, 7],
                        [1, 0, 3, 2, 5, 4, 7, 6],
                        [2, 3, 0, 1, 6, 7, 4, 5],
                        [3, 2, 1, 0, 7, 6, 5, 4],
                        [4, 5, 6, 7, 0, 1, 2, 3],
                        [5, 4, 7, 6, 1, 0, 3, 2],
                        [6, 7, 4, 5, 2, 3, 0, 1],
                        [7, 6, 5, 4, 3, 2, 1, 0]])

def tile_group(m, n, l, t):
    q, r = divmod(max(m, n), 8)
    tile_index = 0
    while tile_index < q:
        # the sum of xors of tile originating at relative position 0, 0
        xor_sum = np.sum(origin_tile)
        
        col_adder = tile_index * 8 * 8 * 8
        
        
        
        tile_time = (224 + \
                     tile_index * 8 * 8 * 8 - \
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