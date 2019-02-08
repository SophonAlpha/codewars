"""
My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

def height(floor, eggs, tries):
    max_tries = min(eggs, tries)
    eggs_left = eggs - max_tries
    attempts_left = tries - max_tries
    floor += attempts_left + 1
    height(floor, eggs_left + 1, attempts_left)
    return floor

print(height(0, 4, 5))
