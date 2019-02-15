"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

def height(floor, attempt, eggs, attempts_left):
    attempt += 1
    attempts_left -= 1
    eggs -= 1
    if 0 <= eggs <= 1 or 0 >= attempts_left <= 1:
        floor += attempts_left + 1
        print(floor)
        if attempts_left > 0:
            floor = height(floor, attempt, eggs + 1, attempts_left)
    else:
        floor = height(floor, attempt, eggs, attempts_left)
        floor += 1
        print(floor)
        if attempts_left > 0:
            floor = height(floor, attempt, eggs + 1, attempts_left)
    return floor

print(height(0, 0, 7, 500))

