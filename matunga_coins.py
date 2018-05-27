import itertools
import numpy as np

def min_price(coins):
    max_iterations = 10000
    iteration = 1
    l = {}
    found_min_price = False
    while not(found_min_price) and iteration <= max_iterations:
        l.update({sum(c): c for c in itertools.combinations_with_replacement(coins, iteration)})
        iteration += 1
        sums = sorted(l.keys())
        for i, _ in enumerate(sums):
            if np.sum(np.diff(sums[i:i+10])) == 9 and len(sums[i:i+10]) == 10:
                return sums[i]
    return -1

print(min_price([3,5])) # 8
print(min_price([4,7])) # 18
print(min_price([5,15])) # -1
print(min_price([6,7,8])) # 18
print(min_price([9,14])) # 104
