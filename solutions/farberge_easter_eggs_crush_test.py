"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

import math
import pprint

def show_matrix(max_eggs, max_tries):
    results = []
    for eggs in range(0, max_eggs + 1):
        results_row = []
        for tries in range(0, max_tries + 1):
#             eggs_2 = eggs if eggs <= tries  else tries
            results_row.append(Catalans_trapezoid(eggs, tries))
        results.append(results_row)
#     pprint.pprint(results_1)
#     print()
    pprint.pprint(results)

def height(eggs, tries):
    floor = 0
    if eggs > 0 and tries > 0:
        eggs = eggs if eggs <= tries else tries
        floor = get_floor(eggs, tries)
        if not floor:
            floor = max_floor(eggs, tries)
#             cur_lookup = {(sub_eggs, sub_eggs + 2): get_floor(sub_eggs, sub_eggs + 2) 
#                           for sub_eggs in range(1, eggs + 1)}
#             for lane in range(tries - (eggs + 2)):
#                 new_lookup = {}
#                 new_lookup[(1, lane + 4)] = lane + 4
#                 for sub_eggs in range(2, eggs + 1):
#                     sub_tries = lane + sub_eggs + 3
#                     new_lookup[(sub_eggs, sub_tries)] = cur_lookup[(sub_eggs, sub_tries - 1)] + \
#                                                         new_lookup[(sub_eggs - 1, sub_tries - 1)] + 1
#                 cur_lookup = new_lookup.copy()
#             floor = new_lookup[(eggs, tries)]
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

def Catalans_trapezoid(n, k):
    """
    Generalisation of Catalan's triangle = Catalan's trapezoid
    https://en.wikipedia.org/wiki/Catalan%27s_triangle
    """
    c = (math.factorial(n + k) // math.factorial(n)) // math.factorial(k)
    return c

def max_floor(eggs, tries):
    floor = 0
    aux = 1
    for i in range(1, eggs + 1):
        aux *= tries + 1 - i
        aux //= i
        floor += aux
    return floor

def binomial_coefficient(n, k):
    """
    http://mathworld.wolfram.com/BinomialCoefficient.html
    """    
    c = math.factorial(n) // (math.factorial(n - k) * math.factorial(k))
    return c

if __name__ == "__main__":
    print(height(2, 14))
#     print(height(477, 3200))
#     show_matrix(10,10)
#     print(height(5, 11))
