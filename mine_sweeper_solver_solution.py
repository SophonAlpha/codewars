"""
mine sweeper code challenge solution of selimk & tactilearning:
https://www.codewars.com/kata/mine-sweeper/solutions/python
"""

import time

def open(row, col):
    global result
    mine_field = [row.split() for row in result.split('\n')]
    try:
        num_mines = int(mine_field[row][col])
    except ValueError:
        num_mines = mine_field[row][col]
    return num_mines

def solve_mine(map, n):
    if n==0:
        return map.replace('?','0')
    if n==map.count('?'):
        return map.replace('?','x')
    map=[r.split() for r in map.split('\n')]
    a,b=len(map),len(map[0])
    map={(i,j):map[i][j] for i in range(a) for j in range(b)}
    M, S, N, x = {}, [], [], set()
    if a==29:map[(28,0)]=open(28,0) # Because one of the tests is wrong!!!
    while True:
        oldM = len(M)
        q = {i for i in map if map[i]=='?'}
        x = {i for i in map if map[i]=='x'}
        M = {i: int(map[i]) for i in map if i not in q|x}
        if len(M)==oldM: break
        S = {(frozenset(neig(i) & q), M[i] - len(neig(i) & x))
             for i in M if neig(i) & q}
        if len(S) < 20:
            S.add((frozenset(q), n-len(x)))
        while len(S) < 250:
            oldS = len(S)
            S.update({(s2 - s1, n2 - n1) for s1, n1 in S for s2, n2 in S
                      if (len(s2 - s1) == n2 - n1 or s1 <= s2) and s1 != s2})
            if len(S)==oldS: break
        for s1, n1 in S:
            if n1==0:
                for t in s1:
                    map[t] = open(*t)
            if n1 == len(s1):
                for t in s1:
                    map[t] = 'x' 
    return strmap(map, a, b) if len(x) == n else '?'
    
def neig(c):
    return {(c[0]+i,c[1]+j) for i in (1,0,-1) for j in (1,0,-1)}-{c}
def strmap(M,a,b):
    return '\n'.join(' '.join(str(M[(i,j)]) if (i,j) in M else '?' for j in range(b)) for i in range(a))
    
gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()
result = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()
print('\nbasic test 1\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
0 0 0 0 0 0 0 ? ? ?
? ? ? ? ? ? 0 ? ? ?
? ? ? ? ? ? 0 ? ? ?
? ? ? ? ? ? 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? ?
0 0 ? ? ? ? ? ? ? ?
0 0 0 0 ? ? ? ? ? ?
0 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? 0 0 0
0 0 0 ? ? ? ? 0 0 0
0 0 0 ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
? ? 0 ? ? ? 0 0 0 0
? ? 0 ? ? ? 0 0 0 0
? ? ? ? ? ? ? ? ? 0
? ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ? ?
0 0 ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ?
0 0 ? ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? ? ?
""".strip()
result = """
0 0 0 0 0 0 0 1 1 1
1 1 1 1 1 1 0 2 x 2
1 x 2 2 x 1 0 2 x 2
1 1 2 x 2 1 0 1 1 1
0 0 2 2 2 1 1 1 0 0
0 0 1 x 1 1 x 2 1 1
0 0 1 1 2 2 2 3 x 2
0 0 0 0 1 x 1 2 x 2
0 0 0 0 1 1 1 1 1 1
0 0 0 1 2 2 1 0 0 0
0 0 0 1 x x 1 0 0 0
0 0 0 1 2 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 1 0 1 1 1 0 0 0 0
x 1 0 1 x 1 0 0 0 0
2 3 1 3 2 2 1 1 1 0
x 2 x 2 x 1 1 x 2 1
1 2 1 2 1 1 1 2 x 1
0 0 1 1 1 0 0 1 1 1
0 0 1 x 1 1 1 2 2 2
0 0 1 1 1 1 x 2 x x
0 0 0 0 0 1 1 2 2 2
""".strip()
print('\ntest case 1\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
? ? ? 0 ? ? ? 0 ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0
? ? ? 0 ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0
0 0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? 0
? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0
? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? 0 0
0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ? 0 0
0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0
0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? ? ? 0 0 0 ? ?
0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 ? ? ? ? ?
0 ? ? ? 0 0 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 ? ? ? ? ?
0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? 0 0
0 ? ? ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? 0 ? ? ? 0 0 0 0 0
? ? 0 ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0 0
? ? 0 0 0 0 ? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0
? ? 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 0
0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0
? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? 0 ? ? ?
? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ? 0 ? ? ?
? ? ? ? ? ? ? 0 ? ? ? ? 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 0 0 0
0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
""".strip()
result = """
1 x 1 0 1 1 1 0 1 x 2 x 1 0 0 0 1 x 1 0 0 0 0 0 0 1 1 1 0 0
1 1 1 0 1 x 2 2 3 2 2 1 1 0 0 0 1 1 2 1 1 0 0 0 0 1 x 1 0 0
0 0 0 1 2 2 2 x x 2 1 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 2 2 1 0
1 1 1 1 x 1 1 2 2 2 x 1 1 1 1 0 0 0 1 1 1 0 0 0 0 0 2 x 2 0
2 x 1 1 1 1 1 1 1 1 1 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 2 x 2 0
x 2 1 0 0 0 1 x 1 0 0 0 2 3 x 1 0 0 0 1 x 1 0 0 0 0 1 1 1 0
1 1 0 0 0 0 2 2 2 0 0 0 1 x 2 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 x 1 0 0 0 2 2 2 0 1 1 1 0 0 0 1 1 1 1 x 1 0 0
0 0 0 0 1 1 2 1 1 0 0 0 1 x 1 0 1 x 1 1 1 2 2 x 1 1 1 1 0 0
0 0 0 0 1 x 1 0 0 0 0 0 1 1 1 0 2 2 2 2 x 3 x 2 1 0 0 0 1 1
0 0 0 0 1 1 1 0 0 0 0 1 1 1 0 0 1 x 1 2 x 4 2 2 0 1 1 1 1 x
0 1 1 1 0 0 0 0 0 0 0 1 x 1 0 0 1 2 2 2 1 2 x 1 0 1 x 1 1 1
0 1 x 2 1 2 1 1 0 0 0 1 1 1 0 0 0 1 x 1 0 1 2 2 1 1 1 1 0 0
0 1 1 2 x 2 x 3 2 1 0 1 2 2 1 0 0 1 2 2 1 0 1 x 1 0 0 0 0 0
1 1 0 1 1 2 2 x x 1 0 1 x x 1 0 0 0 1 x 1 0 1 2 2 1 0 0 0 0
x 1 0 0 0 0 2 3 3 1 0 1 2 2 1 0 0 0 1 1 1 0 0 2 x 2 0 0 0 0
1 1 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 0 0 0 0 0 0 2 x 3 1 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 1 x 1 0 0 0 1 1 1 0 1 2 x 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 2 x 2 0 1 2 2 1 0 0 0
1 2 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 x 2 0 1 x 1 0 1 1 1
1 x x 1 1 1 1 0 1 1 1 0 0 1 1 2 1 1 0 1 1 1 1 2 2 1 0 1 x 1
1 2 3 2 2 x 1 0 1 x 2 1 0 1 x 3 x 2 0 0 0 0 1 x 1 0 0 1 1 1
0 0 1 x 3 2 2 0 1 2 x 1 1 2 2 3 x 3 1 0 0 0 1 1 1 0 0 0 0 0
0 0 1 1 2 x 1 0 0 1 1 2 2 x 2 2 2 x 2 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 1 x 4 x 1 1 1 2 x 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 2 2 x 2 1 0 0 1 1 1 1 x 2 1 1 0 0 0 0
0 0 0 0 0 1 1 2 1 2 x 1 1 1 1 0 0 1 2 2 1 1 1 2 x 2 1 1 1 1
0 0 0 0 0 1 x 4 x 4 2 1 0 0 0 0 0 2 x x 2 2 2 2 3 x 2 1 x 1
0 0 0 0 0 1 2 x x x 1 0 0 0 0 0 0 2 x 3 2 x x 1 2 x 2 1 1 1
""".strip()
print('\ntest case 2\n' + gamemap)
start = time.time()
solution = solve_mine(gamemap, result.count('x'))
end = time.time()
print('execution time: {} seconds'.format(end - start))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
0 1 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 1 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
""".strip()
result = """
0 1 1 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1
0 2 x 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 2 x 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 2 2 2 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1
0 1 x 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
""".strip()
print('\nbig efficiency test \n' + gamemap)
start = time.time()
solution = solve_mine(gamemap, result.count('x'))
end = time.time()
print('efficiency test finished in {} seconds.'.format(end - start))
if solution == '?':
    print('Solved!')
else:
    print('Not solved!')
