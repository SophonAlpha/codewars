"""

Blind4Basic's solution for Four Pass Transport kata:
https://www.codewars.com/kata/four-pass-transport



optimised solution: 1.002065627055475s

"""

from itertools import permutations
from heapq import heappop, heappush
import timeit

INF   = float("inf")
MOVES = [(0,1), (-1,0), (0,-1), (1,0)]        # Turn anticlockwise
ATTENUATION = 0.001

def vertical_dist(pos, p2):
    """
    tie breaker for preference of vertical paths
    """
    c_row, _ = pos
    e_row, _ = p2
    return abs(e_row - c_row) * ATTENUATION

def horizontal_dist(pos, p2):
    """
    tie breaker for preference of horizontal paths
    """
    _, c_col = pos
    _, e_col = p2
    return abs(e_col - c_col) * ATTENUATION

def four_pass(stations):
    def dfs(pOrder, paths, n=0):
        if n==3:
            yield paths[:]
        else:
            _, p1, p2 = pOrder[n]
            for tie_breaker_func in [vertical_dist, horizontal_dist]:
                path = aStar(p1, p2, board, tie_breaker_func)
                if path is None:
                    continue
                paths.append(path)
                updateBoard(board, path)
                yield from dfs(pOrder, paths, n+1)
                updateBoard(board, path, free=1)
                paths.pop()

    pts      = [divmod(s,10) for s in stations]
    segments = [(i, pts[i], pts[i+1]) for i in range(3)]
    MIN      = 1 + sum(manhattan(p1, p2) for _, p1, p2 in segments)

    shortestPath = None
    for pOrder in permutations(segments):
        board = [[1]*10 for _ in range(10)]
        updateBoard(board, pts)

        for p in dfs(pOrder, []):
            length = 4 + sum(map(len, p))
            
            if not shortestPath or length < len(shortestPath):
                shortestPath = rebuildPath(pOrder, p)
                
            if len(shortestPath) == MIN:
                return shortestPath
    
    return shortestPath

def manhattan(*args):
    return sum(abs(b-a) for a,b in zip(*args))

def linearize(p):
    return 10*p[0]+p[1]

def updateBoard(board, inPath, free=0):
    for x, y in inPath: board[x][y] = free
    
def rebuildPath(pOrder, shortest):
    fullPath = []
    for (i, p1, p2),path in sorted(zip(pOrder, shortest)):
        fullPath.append(linearize(p1))
        fullPath.extend(map(linearize,path))
    fullPath.append(linearize(p2))
    return fullPath

def aStar(p1, p2, board, tie_breaker_func):
    prev  = [[None]*10 for _ in range(10)]
    # (heuristic, rotation index)
    local = [[INF if free else 0 for free in r] for r in board]
    local[p2[0]][p2[1]] = INF
    
    # queue: (cost+h, rotation index, cost, (x,y))
    q = [(manhattan(p1, p2) + tie_breaker_func(p1, p2), 0, p1)]
    while q and not q[0][-1] == p2:
        _, cost, src = heappop(q)
        x, y = src
        for a, b in ((x+dx, y+dy)
                     for i, (dx, dy) in enumerate(MOVES)
                     if 0 <= x + dx < 10 and 0 <= y + dy < 10):
            pos, nCost = (a, b), cost + 1
            if nCost < local[a][b]:
                prev[a][b], local[a][b] = src, nCost
                heappush(q, (nCost + manhattan(pos, p2) + tie_breaker_func(pos, p2),
                             nCost, pos))

    if q:
        p, (x,y) = [], q[0][-1]
        while 1:
            x,y = pos = prev[x][y]
            if pos == p1: break
            p.append(pos)
        return p[::-1]

print(four_pass([62, 67, 36, 86]))
results = timeit.timeit(stmt='four_pass([62, 67, 36, 86])',
                        setup='from __main__ import four_pass',
                        number=100)
print('total runtime: {}s'.format(results))
