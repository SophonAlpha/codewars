"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

import math

def height(eggs, tries):
    floor = 0
    if eggs > 0 and tries > 0:
        eggs = eggs if eggs <= tries else tries
#         floor = calculate_Catalan_sums(eggs, tries)
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
#         print('level {}: {} = {}'.format(level, level_count_curr, sum(level_count_curr)))
        print('level {}: {}'.format(level, sum(level_count_curr)))
#         print('floor = {}',format(floor))
        level_count_prev = level_count_curr[:]
        segments -= 1
        eggs -= 1
    return floor

def calculate_Catalan_sums(levels, segments):
    level_sum = 0
    for level in range(1, levels + 1):
        level_sum += Catalans_trapezoid(level, segments - level)
    return level_sum

def Catalans_trapezoid(n, k):
    """
    Generalisation of Catalan's triangle = Catalan's trapezoid
    https://en.wikipedia.org/wiki/Catalan%27s_triangle
    """
    c = (math.factorial(n + k) // math.factorial(n)) // math.factorial(k)
    return c

if __name__ == "__main__":
    print(height(7, 8))
    print()
    print(height(7, 9))
    print()

