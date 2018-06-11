import time

def next_bigger(n):
    s = list(str(n))
    for i in range(len(s)-2,-1,-1):
        if s[i] < s[i+1]:
            t = s[i:]
            m = list(filter(lambda x: x>t[0], t))
            m = min(m)
            t.remove(m)
            t.sort()
            s[i:] = [m] + t
            return int("".join(s))
    return -1

def next_bigger_(n):
    i, ss = n, sorted(str(n))

    if str(n) == ''.join(sorted(str(n))[::-1]):
        return -1;

    while True:
        i += 1;
        if sorted(str(i)) == ss and i != n:
            return i;

startTime = time.time()
print(next_bigger(12000000000000)) #
elapsedTime = time.time() - startTime
print(elapsedTime)

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