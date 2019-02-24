"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

import pprint

def height(eggs, tries):
    tower = [('-', '-', '-', '-')] * 1000
    tower.insert(0, (0, 0, eggs, tries))
    recur_lvl = 0
    floor = 0
    attempt = 0
    if eggs > 0 and tries > 0:
        get_floor(tower, recur_lvl, floor, attempt, eggs, tries)
    return floor

def get_floor(tower, recur_lvl, floor, attempt, eggs, tries):
    level_count = {}
    max_segments = max(eggs, tries)
    max_recurse = min(eggs, tries) - 1
    level_count = {1: [1] * max_segments}
    for recurse_lvl in range(2, max_recurse + 1):
        max_recurse_lvl_segments = max_segments + 1 - recurse_lvl
        for segment in range(max_recurse_lvl_segments, 0, -1):
            # TODO: reverse order of segment processing
#             if recurse_lvl == 1:
#                 segment_count = 1
#             else:
            if segment == max_recurse_lvl_segments or segment == max_recurse_lvl_segments - 1:
                num_segments = len(level_count[recurse_lvl - 1])
                segment_count = sum(level_count[recurse_lvl - 1][2:])
            else:
                segment_count = sum(level_count[recurse_lvl - 1][segment: 0: -1])
            if recurse_lvl not in level_count:
                level_count[recurse_lvl] = []
            level_count[recurse_lvl].append(segment_count)
    pprint.pprint(level_count)
    return

height(5, 6)
