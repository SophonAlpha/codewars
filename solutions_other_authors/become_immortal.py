"""

Solution from StefanPochman for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

"""

def elder_age(m,y,l,t):
    """
    m, y = dimension of magic rectangle
    l    = transmission loss
    t    = max time (wrap around values bigger than t)
    """    
    T = 0
    while y:
        y, Y, x = y & y-1, y, m
        while x:
            x, X = x & x-1, x
            s, S = sorted((X - x, Y - y))
            h = max((x^y | S-1) + 1 - l, 0)
            w = min(h, S)
            T += s * w * (h + h - w - 1) // 2
    return T % t

if __name__ == "__main__":
    print(elder_age(16, 8, 8, 100000)) # 224
