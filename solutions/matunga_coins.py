import itertools
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
    sums = []
    while iteration <= max_iterations:
        s = {sum(c): c for c in itertools.combinations_with_replacement(coins, iteration)}
        l.update(s)
        iteration += 1
        sums = sorted(l.keys())
        for i, _ in enumerate(sums):
            if len(set(sums[i:i+10])) == 10 and (max(sums[i:i+10]) - min(sums[i:i+10])) == 9:
                return sums[i]
    return -1

print(min_price([3,5])) # 8
print(min_price([4,7])) # 18
print(min_price([5,15])) # -1
print(min_price([6,7,8])) # 18
print(min_price([9,14])) # 104
