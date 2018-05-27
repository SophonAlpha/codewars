import itertools
import numpy as np
from fractions import gcd
from functools import reduce

def min_price(coins):
    # in order to represent different prices the coins must not have a
    # greatest common denominator (GCD) bigger than 1
    if reduce(lambda x,y: gcd(x,y), coins) > 1:
        return -1
    
    max_iterations = 10000
    iteration = 1
    l = {}
    found_min_price = False
    while not(found_min_price) and iteration <= max_iterations:
        l.update({sum(c): c for c in itertools.combinations_with_replacement(coins, iteration)})
        iteration += 1
        sums = sorted(l.keys())

# test if consecutive 
# if len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1:


        print('-------------')
        print('no. of elements: ', len(sums))
        for e in sums:
            print(e)
        print('-------------')

        for i, _ in enumerate(sums):
            if np.sum(np.diff(sums[i:i+10])) == 9 and len(sums[i:i+10]) == 10:
                print(l[sums[i]])
                return sums[i]
    return -1

#print(min_price([3,5])) # 8
#print(min_price([4,7])) # 18
#print(min_price([5,15])) # -1
#print(min_price([6,7,8])) # 18
print(min_price([9,14])) # 104
