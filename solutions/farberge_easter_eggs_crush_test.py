"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

def height(eggs, tries):
    tower = [('-', '-', '-', '-')] * 1000
    tower.insert(0, (0, 0, eggs, tries))
    recur_lvl = 0
    floor = 0
    attempt = 0
    if eggs > 0 and tries > 0:
        print('level, attempt, eggs, tries')
        tower, floor = get_floor(tower, recur_lvl, floor, attempt, eggs, tries)
        floor -= 1
        tower_rev = tower[floor::-1]
#         tower_rev.reverse()
        for level, values in enumerate(tower_rev):
            recur_lvl, cur_attempt, eggs, tries = values
            print('{}, {}, {}, {}'.format(recur_lvl, cur_attempt, eggs, tries))
    return floor

def get_floor(tower, recur_lvl, floor, attempt, eggs, tries):
    recur_lvl += 1
    attempts_left = tries - attempt
    if eggs <= 1 or attempts_left <= 1:
        floor += attempts_left + 1
    else:
        for cur_attempt in range(attempt + 1, tries + 1):
            if cur_attempt == attempt + 1:
                tower, floor = get_floor(tower, recur_lvl, floor, cur_attempt, eggs - 1, tries)
            else:
                
            tower.insert(floor, (recur_lvl, cur_attempt, eggs, tries - cur_attempt))
        floor += 1
    return tower, floor

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

print(height(5, 6))
