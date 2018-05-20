def removNb(n):
    r = []
    t = range(1,n+1)
    s = int((n/2)*(1+n))
    for a in t:
        b = (s - a) / (a + 1)
        if (b <= n) and (b % 1 == 0):
            r.append((a, int(b)))
    return r

print(removNb(10))
print(removNb(26))
print(removNb(10000))
