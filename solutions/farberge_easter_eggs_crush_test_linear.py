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
    if eggs <= tries // 2:
        floor = get_floor(1, tries)
        temp_val = floor
        direction = 1
        max_eggs = eggs + 1
    else:
        floor = get_floor(tries - 2, tries)
        temp_val = get_floor(1, tries)
        direction = -1
        max_eggs = tries - eggs    
    for i in range(2, max_eggs):
        temp_val *= tries + 1 - i
        temp_val //= i
        floor += direction * temp_val
    return floor

if __name__ == "__main__":
    print(max_floor(50000, 100000) % MOD)
#     max_floor(4, 20)
#     print(height(4, 6))
