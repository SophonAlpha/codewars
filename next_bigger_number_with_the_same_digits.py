# https://www.codewars.com/kata/next-bigger-number-with-the-same-digits/train/python

def next_bigger(n):
    # find upper bound
    n_str = list(str(n))
    for i in reversed(range(len(n_str))):
        upper_bound = n_str[:]
        for idx, digit in enumerate(n_str[i:]):
            if int(digit) < int(n_str[i]):
                upper_bound[i] = digit
                upper_bound[i + idx] = n_str[i]
    
    return upper_bound

def next_bigger_v2(n):
    n_str = list(str(n))
    next_num = n
    for i1 in reversed(range(len(n_str))):
        next_num_str = list(str(next_num))
        for i2 in reversed(range(len(next_num_str))):
            next_str = next_num_str[:]
            next_str[i1] = next_num_str[i2]
            next_str[i2] = next_num_str[i1]
            num = int(''.join(next_str))
            if next_num == n and num > n:
                next_num = num
            if num > n and num < next_num:
                next_num = num
    return next_num if next_num > n else -1

def next_bigger_v1(n):
    n_str = list(str(n))
    next_num = -1
    for i1 in reversed(range(len(n_str))):
        for i2 in reversed(range(len(n_str))):
            next_str = n_str[:]
            next_str[i1] = n_str[i2]
            next_str[i2] = n_str[i1]
            num = int(''.join(next_str))
            if next_num == -1 and num > n:
                next_num = num
            if num > n and num < next_num:
                next_num = num
    return next_num


print(next_bigger(318007070431)) # 318007071034
print(next_bigger(69777535752)) # 69777537255
print(next_bigger(8292804331163)) # 8292804331316
print(next_bigger(144)) # 414
print(next_bigger(10847638))
print(next_bigger(2071)) # 2170
print(next_bigger(414)) # 441
print(next_bigger(2017)) # 2071
print(next_bigger(513)) # 531
print(next_bigger(12)) # 21
print(next_bigger(555)) # -1
print(next_bigger(9)) # -1
print(next_bigger(111)) # -1
print(next_bigger(531)) # -1