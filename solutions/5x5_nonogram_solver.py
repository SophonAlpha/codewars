"""
Solution for 5x5 Nonogram Solver:
https://www.codewars.com/kata/5x5-nonogram-solver/

Level: 4 kyu

try nonograms here: https://www.puzzle-nonograms.com/
"""


done = False
squares = [1, 2]
runs = [0, 0, 0, 0, 0]
variants = set()

while not done:
    max_pos = len(runs) - (sum(squares) + len(squares) - 1)
    for pos in range(max_pos + 1):
