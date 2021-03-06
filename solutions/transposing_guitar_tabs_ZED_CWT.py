def transpose(amount,tab):
    col,res = 0,[''] * len(tab)
    while col < len(tab[0]):
        t = [v[col] + (v[1 + col] if v[col:2 + col].isdigit() else '') for v in tab]
        col += 1 + any(1 < len(v) for v in t)
        n,j = [],False
        for v in t:
            if v.isdigit():
                v = amount + int(v)
                j = j or 9 < v
                if v < 0 or 22 < v: return 'Out of frets!'
                n.append(str(v))
            else: n.append(v)
        for f,v in enumerate(n): res[f] += v + '-' if j and len(v) < 2 else v
    return res



t = transpose(+2, [
'e|-10-----5-7-----7-|-8-----8-2-----2-|-0---------0-----|-----------------|',
'B|------5-----5-----|---5-------3-----|---1---1-----1---|-0-1-1-----------|',
'G|----5---------5---|-----5-------2---|-----2---------2-|-0-2-2-----------|',
'D|-7--------6-------|-5-------4-------|-3---------------|-----------------|',
'A|------------------|-----------------|-----------------|-2-0-0---0--/8-7-|',
'E|------------------|-----------------|-----------------|-----------------|'])

print(t)

"""
'e|-------7-9-----9-|-10-----10-4-----4-|-2---------2-----|------------------|',
'B|-----7-----7-----|----7--------5-----|---3---3-----3---|-2-3-3------------|',
'G|---7---------7---|------7--------4---|-----4---------4-|-2-4-4------------|',
'D|-9-------8-------|-7---------6-------|-5---------------|------------------|',
'A|-----------------|-------------------|-----------------|-4-2-2---2--/10-9-|',
'E|-----------------|-------------------|-----------------|------------------|'
"""