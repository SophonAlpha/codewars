"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

import pprint

def height(eggs, tries):
    floor = 0
    if eggs > 0 and tries > 0:
        recur_lvl = 0
        floor = 0
        attempt = 0
        floor = get_floor(recur_lvl, floor, attempt, eggs, tries)
#         print(floor)
#         print()
#         recur_lvl = 0
#         floor = 0
#         attempt = 0
#         floor = get_floor_v1(recur_lvl, floor, attempt, eggs, tries) - 1
#         print(floor)
    return floor

def get_floor(recur_lvl, floor, attempt, eggs, tries):
    floor = 0
    segments = max(eggs, tries)
    max_level = min(eggs, tries) - 1
    level_count = {}
    for level in range(1, max_level + 1):
        for segment in range(segments):
            attempt = segment + level
            if level > 1:
                start = segment if segment < segments - 2 else segments - 2
                segment_count = sum(level_count[level - 1][start:: -1])
            else:
                segment_count = 1
            if level not in level_count:
                level_count[level] = []
            level_count[level].append(segment_count)
            if eggs - 1 <= 1 or tries - attempt <= 1:
                floor_height = tries - attempt + 1
            else:
                floor_height = 1
            floor += floor_height * segment_count
        segments -= 1
        eggs -= 1
#     pprint.pprint(level_count)
    return floor

def get_floor_v1(recur_lvl, floor, attempt, eggs, tries):
    recur_lvl += 1
    attempts_left = tries - attempt
    if eggs <= 1 or attempts_left <= 1:
        floor += attempts_left + 1
    else:
        for cur_attempt in range(attempt + 1, tries + 1):
            floor = get_floor_v1(recur_lvl, floor, cur_attempt, eggs - 1, tries)
#             print('lvl: {}, floor: {}, attempt: {}'.format(recur_lvl, floor, cur_attempt))
        floor += 1
    return floor

print(height(5, 6)) # 62
print(height(7, 20)) # 137979
