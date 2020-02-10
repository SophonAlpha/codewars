"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""

import functools

done = False
squares = [1, 2]
run_len = 5
variants = set()

a = [1, 2, 4, 8, 16, 32, 64, 128]
b = functools.reduce(lambda x, y: x | y, a)
fmt = '{0:0' + str(run_len) + 'b}'
print(fmt.format(b))



while not done:
    max_pos = len(runs) - (sum(squares) + len(squares) - 1)
    for pos in range(max_pos + 1):
