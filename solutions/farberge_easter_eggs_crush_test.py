"""
My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

def next_floor(floor, eggs, attempts):
    max_attempts = min(eggs, attempts)
    all_fail_floors = [2**attempt for attempt in range(max_attempts)]
    return floor + 2**(max_attempts - 1) 
