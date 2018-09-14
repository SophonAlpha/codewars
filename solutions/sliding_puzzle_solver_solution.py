class Solver:
    def __init__(self, n, puzzle):
        self.n = n
        self.tiles = {}
        for r in range(n):
            for c in range(n):
                self.tiles[r, c] = puzzle[r][c]
        self.neighbours = {}
        for r in range(n):
            for c in range(n):
                neighs = []
                for (dr, dc) in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    neigh = (r + dr, c + dc)
                    if neigh in self.tiles:
                        neighs.append(neigh)
                self.neighbours[r, c] = neighs[:]
        self.manhDist = {}
        for (r1, c1) in self.neighbours:
            for (r2, c2) in self.neighbours:
                self.manhDist[r1, c1, r2, c2] = abs(r1 - r2) + abs(c1 - c2)
        self.answer = []

    def solved(self):
        for (r, c) in self.tiles:
            if r == self.n - 1 and c == self.n - 1:
                if self.tiles[r, c] != 0:
                    return False
            elif r * self.n + c + 1 != self.tiles[r, c]:
                return False
        return True

    def solve(self):
        for i in range(self.n):
            self.solveRow(i)
            if self.solved():
                break
            self.solveColumn(i)
            if self.solved():
                break
        return self.answer

    def findTile(self, tile):
        for (r, c) in self.tiles:
            if self.tiles[r, c] == tile:
                return (r, c)

    def solveRow(self, r):
        for c in range(r, self.n - 2):
            self.solveTile((r, c), r * self.n + c + 1)
        last_1 = (r + 1) * self.n
        last_1pos = (r + 1, self.n - 1)
        last_2 = last_1 - 1
        last_2pos = (r, self.n - 1)
        bottom_right = (self.n - 1, self.n - 1)
        self.solveTile(bottom_right, last_1, [], True)
        self.solveTile(last_2pos, last_2, [], True)
        self.solveTile(last_1pos, last_1, [last_2pos], True)
        self.moveBlank(r, self.n - 2, [last_1pos, last_2pos])
        for c in range(self.n - 2, self.n):
            self.solveTile((r, c), r * self.n + c + 1)

    def solveColumn(self, c):
        for r in range(c + 1, self.n - 2):
            self.solveTile((r, c), r * self.n + c + 1)
        last_1 = self.n * (self.n - 1) + c + 1
        last_1pos = (self.n - 1, c + 1)
        last_2 = last_1 - self.n
        last_2pos = (self.n - 1, c)
        bottom_right = (self.n - 1, self.n - 1)
        self.solveTile(bottom_right, last_1, [], True)
        self.solveTile(last_2pos, last_2, [], True)
        self.solveTile(last_1pos, last_1, [last_2pos], True)
        self.moveBlank(self.n - 2, c, [last_1pos, last_2pos])
        for r in range(self.n - 2, self.n):
            self.solveTile((r, c), r * self.n + c + 1)

    def solveTile(self, destPos, targetTile, lockedPos = [], temp = False):
        r, c = destPos
        while True:
            (rx, cx) = self.findTile(targetTile)
            if (rx, cx) == (r, c):
                break
            neighbours = self.neighbours[rx, cx]
            if rx > r and (rx - 1, cx) in neighbours:
                newr, newc = rx - 1, cx
            elif rx < r and (rx + 1, cx) in neighbours:
                newr, newc = rx + 1, cx
            elif cx > c and (rx, cx - 1) in neighbours:
                newr, newc = rx, cx - 1
            elif cx < c and (rx, cx + 1) in neighbours:
                newr, newc = rx, cx + 1
            self.moveBlank(newr, newc, lockedPos + [(rx, cx)])
            self.moveTile(rx, cx, newr, newc)
        if not temp:
            for neighbour in self.neighbours[r, c]:
                self.neighbours[neighbour].remove((r, c))
            self.neighbours[r, c] = []

    def moveBlank(self, r, c, lockedPos):
        (rx, cx) = self.findTile(0)
        path = self.findPath(rx, cx, r, c, lockedPos)
        if path:
            for neighbourPos in path[1:]:
                neighbourTile = self.tiles[neighbourPos]
                self.tiles[neighbourPos] = 0
                self.tiles[rx, cx] = neighbourTile
                self.answer += [neighbourTile]
                rx, cx = neighbourPos

    def moveTile(self, oldr, oldc, newr, newc):
        neighbourTile = self.tiles[oldr, oldc]
        self.tiles[oldr, oldc] = 0
        self.tiles[newr, newc] = neighbourTile
        self.answer += [neighbourTile]

    def findPath(self, oldr, oldc, newr, newc, lockedPos):
        queue = [[0, (oldr, oldc), [(oldr, oldc)]]]
        while queue:
            thisNode = queue.pop(0)
            dist, thisPos, path = thisNode
            for neighPos in self.neighbours[thisPos]:
                if neighPos not in lockedPos:
                    if neighPos == (newr, newc):
                        return path[:] + [neighPos]
                    if neighPos not in path:
                        nr, nc = neighPos
                        dist = self.manhDist[nr, nc, newr, newc]
                        queue.append([dist, neighPos, path[:] + [neighPos]])
            queue.sort(key = lambda q: q[0])

def slide_puzzle(puzzle):
    n = len(puzzle)

    # check solvability
    size = n * n - 1
    flat = [x for row in puzzle for x in row if x != 0]
    inversions = sum(flat[i] > x for i in range(size) for x in flat[i + 1:])
    for r in range(n):
        if 0 in puzzle[r]:
            zeroRow = r
            break
    if n % 2 == 1:
        if inversions % 2 == 1: return None
    else:
        if inversions % 2 == (n - zeroRow) % 2: return None

    # set up solver
    solver = Solver(n, puzzle)
    answer = solver.solve()
    return answer
