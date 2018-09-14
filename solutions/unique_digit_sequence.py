# https://www.codewars.com/kata/unique-digit-sequence/train/python
import functools

def find_num(n):
    # build sequence
    s = []
    num = 0 # number
    while len(s) <= n:
        if len(s) == 0:
            s.append(num)
        else:
            num = 0
            while True:
                # check if number is already part of the series
                if num in s:
                    num += 1
                    continue

                # check if number contains any digits of the previous one
                if not(set(str(num)) & set(str(s[-1]))):
                    s.append(num)
                    break
                num += 1

    return s[n]

print(find_num(1)) # 1
print(find_num(5)) # 5
print(find_num(11)) # 22
print(find_num(100)) # 103
print(find_num(500)) # 476
