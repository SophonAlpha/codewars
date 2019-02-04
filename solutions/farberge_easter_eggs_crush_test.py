"""
My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

def height(eggs, tries):
    
    
    
    floor = 0
    while tries > 0 and eggs > 0:
        max_attempts = min(eggs, tries)
        floor += 2**(max_attempts - 1)
        print(floor)
        tries -= 1
    return floor
