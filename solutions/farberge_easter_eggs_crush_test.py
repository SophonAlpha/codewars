"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

import math
import pprint

def show_matrix(max_eggs, max_tries):
    results_1 = []
    results_2 = []
    for eggs in range(1, max_eggs + 1):
        results_row = [get_floor(eggs, tries) for tries in range(1, max_tries + 1)]
        print(results_row)
        results_1.append(results_row)
        results_row = []
        for tries in range(1, max_tries + 1):
            eggs_2 = eggs if eggs <= tries  else tries
            results_row.append(Catalans_trapezoid(eggs_2, tries - 1))
        results_2.append(results_row)
#     pprint.pprint(results_1)
#     print()
#     pprint.pprint(results_2)

def height(eggs, tries):
    floor = 0
    if eggs > 0 and tries > 0:
        eggs = eggs if eggs <= tries else tries
#         floor = calculate_Catalan_sums(eggs, tries)
        floor = get_floor(eggs, tries)
    return floor

def height_v2(eggs, tries):
    eggs = eggs if eggs <= tries else tries
    to_do = [(eggs, tries)]
    lookup = {}
    while to_do:
        floor = get_floor_v2(to_do[-1], tries)
        if floor:
            lookup[to_do[0]] = floor
            to_do.pop()
    floor_lookup = {}
    floor_lookup[(eggs, eggs)] = 2**eggs - 1
    floor_lookup[(eggs - 1, eggs)] = floor_lookup[(eggs, eggs)] - 1
    floor_lookup[(eggs - 2, eggs)] = floor_lookup[(eggs, eggs)] - 1
    for step in range(eggs + 1, tries + 1):
        val1 = floor_lookup[(eggs, step - 1)]
        val2 = floor_lookup[(eggs - 1, step - 1)]
        floor_lookup[(eggs, step)] = val1 + val2
        
    floor = val1
    return floor

def get_floor_v2(eggs, tries):
    if eggs == 1:
        floor = tries
    elif eggs == tries:
        floor = 2**tries - 1
    elif eggs == (tries - 1):
        floor = 2**tries - 1 - 1
    elif eggs == (tries - 2):
        floor = 2**tries - 1 - tries
    elif eggs == (tries - 3):
        floor = (2**tries - 1 - tries) - (2**(tries - 1) - 1 - 1)
    else:
        floor = None
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
#         print('level {}: {}'.format(level, sum(level_count_curr)))
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
#     print(height_v2(3,+ 10))
    
    
    show_matrix(20,20)
#     print()
    
#     print(height(7, 8))
#     print()
#     print(height(7, 9))
#     print()

