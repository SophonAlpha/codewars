"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

sources:
	https://medium.com/@duhroach/fast-fun-with-pascals-triangle-6030e15dced0
	https://stackoverflow.com/questions/15580291/how-to-efficiently-calculate-a-row-in-pascals-triangle
	https://www.mathsisfun.com/pascals-triangle.html
	https://brilliant.org/wiki/egg-dropping/

"""

def height(eggs, tries):
    floor = 0
    if eggs > 0 and tries > 0:
        eggs = eggs if eggs <= tries else tries
        floor = get_floor(eggs, tries)
        if not floor:
            floor = max_floor(eggs, tries)
    return floor

def get_floor(eggs, tries):
    if eggs == 1:
        floor = tries
    elif eggs == tries:
        floor = 2**tries - 1
    elif eggs == (tries - 1):
        floor = 2**tries - 1 - 1
    elif eggs == (tries - 2):
        floor = 2**tries - 2 - tries
    elif eggs == (tries - 3):
        floor = (2**tries - 1 - tries) - (2**(tries - 1) - 1 - 1)
    else:
        floor = None
    return floor

def max_floor(eggs, tries):
    floor = 0
    temp_val = 1
    for i in range(1, eggs + 1):
        temp_val *= tries + 1 - i
        temp_val //= i
        floor += temp_val
    return floor

if __name__ == "__main__":
    print(height(2, 14))
