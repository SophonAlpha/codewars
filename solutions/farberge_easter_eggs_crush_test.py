"""
My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

def next_floor(floor, eggs, attempts):
    max_attempts = min(eggs, attempts)
    
    
    
    before_last_floor = floor + (attempts - eggs - 1)
    return before_last_floor + (before_last_floor - floor)
