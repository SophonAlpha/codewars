"""
My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

def height(eggs, tries):
    floor = 0
    max_tries = min(eggs, tries)
    for attempt in range(max_tries, 0, -1):
        eggs_left = eggs - attempt
        attempts_left = tries - attempt
        if eggs_left == 1:
            floor += attempts_left + 1
        else:
            # recursive call
            pass
        print(floor, attempt, eggs_left, attempts_left)

def get_floor(floor, attempt, eggs_left, attempts):
    floor = floor


#     
#     max_attempts = min(eggs, tries)
#     floor_before_last_attempt_all_fail = tries - (max_attempts - 1)
#     
#     
#     
#     floor = 0
#     while tries > 0 and eggs > 0:
#         max_attempts = min(eggs, tries)
#         floor += 2**(max_attempts - 1)
#         print(floor)
#         tries -= 1
#     return floor
