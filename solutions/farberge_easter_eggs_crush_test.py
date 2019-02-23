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
    for recurse_lvl in range(1, max_recurse + 1):
        max_recurse_lvl_segments = max_segments + 1 - recurse_lvl
        for segment in range(max_recurse_lvl_segments, 0, -1):
            if recurse_lvl == 1:
                segment_count = 1
            else:
                if segment == max_recurse_lvl_segments or segment == max_recurse_lvl_segments - 1:
                    segment_count = len(level_count[recurse_lvl - 1]) - 2
                else:
                    segment_count = sum(level_count[recurse_lvl - 1][segment: 0: -1])
            if recurse_lvl not in level_count:
                level_count[recurse_lvl] = []
            level_count[recurse_lvl].append(segment_count)
    pprint.pprint(level_count)
    return

def get_floor_v2(tower, recur_lvl, floor, attempt, eggs, tries):
    recur_lvl += 1
    attempts_left = tries - attempt
    if eggs <= 1 or attempts_left <= 1:
        floor += attempts_left + 1
    else:
        for cur_attempt in range(attempt + 1, tries + 1):
            tower, floor = get_floor(tower, recur_lvl, floor, cur_attempt, eggs - 1, tries)
            tower.insert(floor, (recur_lvl, cur_attempt, eggs, tries - cur_attempt))
        floor += 1
    return tower, floor

def get_floor_v1(recur_lvl, floor, attempt, eggs, tries):
    recur_lvl += 1
    attempts_left = tries - attempt
    if eggs <= 1 or attempts_left <= 1:
        floor += attempts_left + 1
    else:
        for cur_attempt in range(attempt + 1, tries + 1):
            floor = get_floor(recur_lvl, floor, cur_attempt, eggs - 1, tries)
#             if recur_lvl == 1:
            print('lvl: {}, floor: {}, attempt: {}'.format(recur_lvl, floor, cur_attempt))
#             if recur_lvl == 2:
#                 print('lvl: {}, floor: {}, attempt: {}'.format(recur_lvl, floor, cur_attempt))
        floor += 1
    return floor

height(5, 6)
