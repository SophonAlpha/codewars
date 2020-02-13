"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""

import functools


def init_shift(squares, max_len):
    start_pos = 0
    squares_shftd = []
    for run in squares:
        shift = max_len - start_pos - run
        squares_shftd.append((2 ** run - 1) << shift)
        start_pos = start_pos + run + 1
    return squares_shftd


def merge(squares):
    return functools.reduce(lambda x, y: x | y, squares)


def visualize(squares_shftd, max_len):
    fmt = '{0:0' + str(max_len) + 'b}'
    for item in squares_shftd:
        print(f'{item:5} = {fmt.format(item)}')


def get_positions(squares, idx, start_r_shift, max_r_shift):
    positions = []
    squares_shftd = squares[:]
    for r_shift in range(start_r_shift, max_r_shift + 1):
        if (len(squares) - idx) > 1:
            positions = positions + get_positions(squares, idx + 1, r_shift, max_r_shift)
            get_positions(squares, idx + 1, r_shift, max_r_shift)
        squares_shftd[idx] = squares[idx] >> r_shift
        positions.append(merge(squares_shftd))
        # print(f'index = {idx}, r_shift = {r_shift}')
    return positions


squares = [1, 3, 2]
max_len = 11
max_r_shift = max_len - (sum(squares) + len(squares) - 1)
squares_shftd = init_shift(squares, max_len)
get_positions(squares_shftd, 0, 0, max_r_shift)

visualize(squares_shftd, max_len)
