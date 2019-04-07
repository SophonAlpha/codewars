"""

My solution for 'Faberge easter eggs crush test [linear]' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test-linear

Level: 1 kyu

"""

MOD = 998244353

def height(eggs, tries):
    floor = 0
    if eggs > 0 and tries > 0:
        eggs = eggs if eggs <= tries else tries
        floor = get_floor(eggs, tries)
        if not floor:
            floor = max_floor(eggs, tries)
    return floor % MOD

def get_floor(eggs, tries):
    if eggs == 1:
        floor = tries
    elif eggs == tries:
        floor = 2**tries - 1
    elif eggs == (tries - 1):
        floor = 2**tries - 2
    elif eggs == (tries - 2):
        floor = 2**tries - 2 - tries
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
    print(height(16, 19))
