"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

import math

def height(eggs, tries):
    floor = 0
    if eggs > 0 and tries > 0:
        floor = get_floor(eggs, tries)
    return floor

def get_floor(eggs, tries):
    floor = 0
    segments = tries
    max_level = min(eggs, tries)
    level_count_prev = []
    for level in range(1, max_level + 1):
        level_count_curr = []
        for segment in range(segments):
            if level > 1 and segment > 0:
                segment_count = level_count_curr[segment - 1] + \
                                level_count_prev[segment]
            else:
                segment_count = 1
            level_count_curr.append(segment_count)
            floor += segment_count
        print('level {}: {} = {}'.format(level, level_count_curr, sum(level_count_curr)))
        level_count_prev = level_count_curr[:]
        segments -= 1
        eggs -= 1
    return floor

def sum_arith_seq(num, start, end):
    return (num * (start + end)) / 2

def transform_Catalans_tri(levels, segments):
    for level in range(0, levels):
        seq = [int(generate_Catalans_triangle(level, segment)) for segment in range(0, segments)]
        print('level {}: {} = {}'.format(level, seq, sum(seq)))
    return

def generate_Catalans_triangle(n, k):
    c = (math.factorial(n + k) * (n - k + 1)) / (math.factorial(k) * math.factorial(n + 1))
    return c

if __name__ == "__main__":

    print(height(9, 9))
    print()
    print(height(5, 7))
    print()
