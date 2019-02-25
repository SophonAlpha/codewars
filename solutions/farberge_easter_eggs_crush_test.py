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
    segments = max(eggs, tries)
    max_recurse = min(eggs, tries) - 1
    level_count = {1: [1] * segments}
    for recurse_lvl in range(2, max_recurse + 1):
        segments = segments - 1
        for segment in range(segments):
            start = segment if segment < segments - 2 else segments - 2
            segment_count = sum(level_count[recurse_lvl - 1][start:: -1])
            if recurse_lvl not in level_count:
                level_count[recurse_lvl] = []
            level_count[recurse_lvl].append(segment_count)
    pprint.pprint(level_count)
    return

height(5, 6)
