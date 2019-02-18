# codewars code gymnastics
Notes from solving the www.codewars.com katas.

### Four Pass Transport

Blind4Basics published an interesting solution with just 70 source lines of code (sloc) vs. the 470 sloc I needed for my approach. A few things I picked up from this solution.

A better way to convert the single integer positions (e.g. '34') to two integers (e.g. row = 3, column = 4). My approach:

```python
pos = 34
row = pos // 10
col = pos % 10
```

... better:

```python
row, col = divmod(34, 10)
```

Use `heapq` module to implement the A* search open set queue as a heap. This allows to make use of the key attribute of a heap that the smallest element is always the root (`heap[0]`)
```python
q = [(manhattan(p1,p2), 0, 0, p1)]
    while q and not q[0][-1] == p2:
        _, _, cost, src = heappop(q)
        x, y = src
        for i, a, b in ((i, x+dx, y+dy)
                        for i, (dx, dy) in enumerate(moves)
                        if 0<=x+dx<10 and 0<=y+dy<10):
            pos, nCost = (a,b), cost+1
            if (nCost, i) < local[a][b]:
                prev[a][b], local[a][b] = src, (nCost,i)
                heappush(q, (nCost+manhattan(pos, p2), i, nCost, pos))
```
