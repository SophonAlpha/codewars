# https://www.codewars.com/kata/next-bigger-number-with-the-same-digits/train/python

def next_bigger(n):
    next_num = -1
    n_str = list(str(n))
    # step through each digit from right to left
    for i1 in reversed(range(len(n_str))):
        right_part = n_str[i1 + 1:]
        # find the smallest number in the right part that is bigger than
        # the current digit
        bigger_number = None
        pos = None
        for i2, digit in enumerate(right_part):
            if int(digit) > int(n_str[i1]):
                if bigger_number == None:
                    bigger_number = int(digit)
                    pos = i1 + i2 + 1
                else:
                    bigger_number = int(digit) if int(digit) < bigger_number else bigger_number
                    pos = i1 + i2 + 1
        if not(bigger_number == None): break

    if not(bigger_number == None):
        next_num = n_str[:]
        # swap the digits
        next_num[i1] = n_str[pos]
        next_num[pos] = n_str[i1]
        # sort the right part by order
        next_num = next_num[:i1 + 1] + sorted(next_num[i1 + 1:])
        # transform to integer
        next_num = int(''.join(next_num))
    else:
        next_num = -1

    return next_num

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