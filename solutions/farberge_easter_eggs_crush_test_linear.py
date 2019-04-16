"""

My solution for 'Faberge easter eggs crush test [linear]' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test-linear

Level: 1 kyu

"""

from solutions.performance import Profile
PERFORMANCE_STATS = []

MOD = 998244353

def height(eggs, tries):
    """
    Main function
    """
    floor = 0
    if eggs > 0 and tries > 0:
        eggs = eggs if eggs <= tries else tries
        floor = get_floor(eggs, tries)
        if not floor:
            floor = max_floor(eggs, tries)
    return floor % MOD

def get_floor(eggs, tries):
    """
    Border cases that can be calculated without iteration.
    """
    if eggs == 1:
        floor = tries
    elif eggs == tries:
        floor = (2**tries - 1)
    elif eggs == (tries - 1):
        floor = (2**tries - 2)
    elif eggs == (tries - 2):
        floor = (2**tries - 2 - tries)
    else:
        floor = None
    return floor

@Profile(stats=PERFORMANCE_STATS)
def max_floor(eggs, tries):
    """
    Calculate max floor utilising relations related to binomials (see also 
    Pascal triangle).
    Variable 'pre_calc' is used to "modulo down" the value for variable 'val' 
    during iteration as large integers become computational expensive.
    """
    pre_calc = [0, 1]
    for i in range(2, eggs + 1):
        pre_calc.append((MOD - MOD // i) * pre_calc[MOD % i] % MOD)
    floor = 0
    val = 1
    for i in range(1, eggs + 1):
        val = val * (tries + 1 - i) * pre_calc[i] % MOD
        floor = (floor + val) % MOD
    return floor

@Profile(stats=PERFORMANCE_STATS)
def height_slow(eggs, tries):
    """
    Algorithm without "modulo down". Significantly slower.
    """
    floor = get_floor(1, tries)
    temp_val = floor
    max_eggs = eggs + 1
    for i in range(2, max_eggs):
        temp_val = temp_val * (tries + 1 - i)
        temp_val = temp_val // i
        floor = (floor + temp_val) % MOD
    return floor

if __name__ == "__main__":
    print(height(50000, 100000))
    for stat in PERFORMANCE_STATS:
        print(stat)
