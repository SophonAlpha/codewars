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
            floor += attempts_left
        else:
            # recursive call
            pass
        print(floor, attempt, eggs_left, attempts_left)
