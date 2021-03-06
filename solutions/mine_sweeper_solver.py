"""
Solution for codewars mine sweeper challenge:
https://www.codewars.com/kata/mine-sweeper

Level: 1 kyu

If you haven't played Mine Sweeper before or forgot about it:
http://minesweeperonline.com
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

import itertools

def solve_mine(map, n):
    """
    Main function.
    """
    mine_field = MineSweeper(map, n)
    mine_field.solve()
    solved = mine_field.get_state()
    return solved

class MineSweeper:
    """
    Mine sweeper solver class.
    """

    def __init__(self, field_map, total_mines):
        """
        Class setup.
        """
        self.mine_field = [row.split() for row in field_map.split('\n')]
        self.mines_left = total_mines
        self.cells_to_process = [] # A queue of cells that can be opened safely.
        self.previous_queue_state = []
        self.previous_mines_left = None
        self.repetitions = 0
        self.unsolvable = False

    def solve(self):
        """
        Main solver function. It tests different approaches.
        """
        while not self.done():
            self.no_open_cells()
            self.all_cells_are_mines()
            self.no_mines()
            if not self.done():
                self.obvious_cells()
            if not self.done():
                made_progress = self.safe_neighbour_difference()
                if made_progress:
                    continue
            if not self.done():
                made_progress = self.adjacent_combinations()
                if made_progress:
                    continue
        return

    def done(self):
        """
        Detect if we are done. Either all cells are open or the mine field is
        unsolvable.
        """
        return not self.get_all_closed_cells() or self.unsolvable

    def no_open_cells(self):
        """
        Rule:

        Mine filed with no open cells. If there are more cells then mines this
        is not solvable.
        """
        field_size = len(self.mine_field) * len(self.mine_field[0])
        if not self.get_all_open_cells() and self.mines_left < field_size and \
           self.mines_left > 0:
            # Special case: no open cells, mine field  bigger than number of
            # mines and at least one mine.
            self.mine_field = ['?']
            self.unsolvable = True
        return

    def all_cells_are_mines(self):
        """
        Rule:

        All cells are mines.
        """
        closed_cells = self.get_all_closed_cells()
        if self.mines_left == len(closed_cells):
            # Special case: all cells are mines.
            for row, col in closed_cells:
                self.mark_mines([(row, col)])
        return

    def no_mines(self):
        """
        Rule:

        No mines at all.
        """
        if self.mines_left == 0:
            for row, col in self.get_all_closed_cells():
                num_mines = open(row, col)
                self.mine_field[row][col] = num_mines
        return

    def obvious_cells(self):
        """
        Rule:

        Open safe cells and mark mine cells that are obvious, meaning they can
        be deducted solely from the number of mines that surrounds the cell and
        the state of the surrounding cells. E.g. number of mines = 1 and the
        surrounding cells already contain one mine then all surrounding closed
        cells are safe to open.
        """
        self.initialise_queue()
        while self.queue_progress():
            row, col = self.get_next_cell()
            num_mines = open(row, col)
            self.mine_field[row][col] = num_mines
            _, closed_cells, mine_cells, _ = self.get_cells(row, col)
            if num_mines == len(mine_cells):
                # All mines surrounding the cell have been found already. It is
                # safe to open the remaining surrounding closed cells.
                self.queue_cells(closed_cells)
            elif num_mines - len(closed_cells) - len(mine_cells) == 0:
                # Mine cells deduction: all closed cells contain mines. Mark them
                # accordingly.
                self.mark_mines(closed_cells)
            else:
                # Nothing could be done. Put the cell back at the end of the
                # processing queue.
                self.queue_cells([(row, col)])
        return

    def safe_neighbour_difference(self):
        """
        Rule:

        The difference between closed cells of the current cell and closed cells
        of a neighbour cell are safe cells IF number of remaining mines (must
        be > 0) are equal between current and neighbour AND the neighbour closed
        cells are a strict subset of current cell closed cells.
        """
        made_progress = False
        self.initialise_queue()
        for row, col in self.cells_to_process:
            _, closed_cells, mine_cells, numbered_cells = self.get_cells(row, col)
            num_mines = open(row, col)
            mines_outstanding = num_mines - len(mine_cells)
            for n_row, n_col in numbered_cells:
                _, n_closed_cells, n_mine_cells, _ = self.get_cells(n_row, n_col)
                n_num_mines = open(n_row, n_col)
                n_mines_outstanding = n_num_mines - len(n_mine_cells)
                if n_closed_cells and \
                   n_mines_outstanding == mines_outstanding and \
                   mines_outstanding > 0 and \
                   set(n_closed_cells).issubset(set(closed_cells)):
                    safe_cells = list(set(closed_cells).difference(set(n_closed_cells)))
                    for d_row, d_col in safe_cells:
                        num_mines = open(d_row, d_col)
                        self.mine_field[d_row][d_col] = num_mines
                        made_progress = True
        return made_progress

    def adjacent_combinations(self):
        """
        Rule:

        Test all possible combinations of mines for closed cells adjacent to
        numbered cells. Testing all possible combinations gets computational
        expensive if there are a large number of mines left and there is a large
        number of closed cells. Limiting combinations to adjacent closed cells
        reduces the number of combinations (hopefully in many cases).
        """
        adj_closed_cells = self.get_adjacent_closed_cells(self.get_all_numbered_cells())
        made_progress = self.combinations(adj_closed_cells)
        return made_progress

    def get_adjacent_closed_cells(self, numbered_cells):
        """
        Get all closed cells that are adjacent to a list of cells given as
        input.
        """
        adjacent_closed_cells = []
        for row, col in numbered_cells:
            _, closed_cells, _, _ = self.get_cells(row, col)
            adjacent_closed_cells += closed_cells
        return list(set(adjacent_closed_cells))

    def combinations(self, closed_cells):
        """
        Test all possible combinations of mines in the given list of closed
        cells.
        """
        made_progress = False
        mine_combinations = self.get_combinations(closed_cells)
        combination_cells = [cell for combination in mine_combinations
                             for cell in combination]
        safe_cells = set(closed_cells) - set(combination_cells)
        if safe_cells:
            for row, col in safe_cells:
                num_mines = open(row, col)
                self.mine_field[row][col] = num_mines
                made_progress = True
        elif len(mine_combinations) > 1:
            # Not solvable situation: more then one possible combination of mine
            # positions for the remaining closed cells.
            self.unsolvable = True
            self.mine_field = '?'
            made_progress = True
        elif set(self.get_all_closed_cells()) == set(closed_cells) and \
           len(mine_combinations) == 1:
            # Only one possible combination for mine positions in the remaining
            # closed cells. Mark mines.
            self.mark_mines(mine_combinations[0])
            made_progress = True
        return made_progress

    def get_combinations(self, closed_cells):
        """
        Test all combinations of remaining mines in the remaining closed cells.
        Return all possible solutions.
        """
        combinations = []
        range_start = self.mines_left \
                      if set(self.get_all_closed_cells()) == set(closed_cells) \
                      else 1
        range_end = self.mines_left if self.mines_left < len(closed_cells) \
                    else len(closed_cells)
        for num in range(range_start, range_end + 1):
            combinations += list(itertools.combinations(closed_cells, r=num))
        numbered_cells = self.get_numbered_cells_adjacent_closed_cells()
        mine_combinations = self.test_combinations(combinations, numbered_cells)
        return mine_combinations

    def get_numbered_cells_adjacent_closed_cells(self):
        """
        Return all numbered cells that are next to closed cells.
        """
        numbered_cells_adjacent_closed_cells = []
        numbered_cells = self.get_all_numbered_cells()
        for row, col in numbered_cells:
            _, closed_cells, _, _ = self.get_cells(row, col)
            if closed_cells:
                numbered_cells_adjacent_closed_cells.append((row, col))
        return numbered_cells_adjacent_closed_cells

    def test_combinations(self, combinations, cells):
        """
        Test a list of mine field combinations and return only the ones that
        are valid.
        """
        mine_combinations = []
        for combination in combinations:
            combination_fit = False
            for row, col in cells:
                # Test whether a combination of mines satisfies the number of
                # know mines for neighbouring open numbered cells.
                _, closed_cells, mine_cells, _ = self.get_cells(row, col)
                remaining_mines = open(row, col) - len(mine_cells)
                possible_safe_cells = set(combination) & set(closed_cells)
                if len(possible_safe_cells) == remaining_mines:
                    combination_fit = True
                else:
                    combination_fit = False
                    break
            if combination_fit:
                mine_combinations.append(combination)
        return mine_combinations

    def initialise_queue(self):
        """
        Load a queue with all cells that are open and have closed cells around
        them and are a number cell (= not a mine).
        """
        self.cells_to_process = []
        for row, col in self.get_all_open_cells():
            _, closed_cells, _, _ = self.get_cells(row, col)
            if not self.mine_field[row][col] == 'x' and closed_cells:
                self.queue_cells([(row, col)])
        return

    def get_next_cell(self):
        """
        Get the next cell from the processing queue.
        """
        cell = self.cells_to_process.pop(0)
        return cell

    def queue_cells(self, cells):
        """
        Queue safe cells for processing.
        """
        self.cells_to_process += [cell for cell in cells
                                  if not cell in self.cells_to_process]
        return

    def queue_progress(self):
        """
        Detect if the processing queue is progressing.

        Return values:

        True  = There is progress in the queue
        False = No progress in the queue. The same elements circulating in the
                queue (taken from the front and appended at the end)
        """
        ret = True
        if set(self.previous_queue_state) == set(self.cells_to_process) and \
           self.previous_mines_left == self.mines_left:
            self.repetitions += 1
        else:
            self.previous_queue_state = self.cells_to_process.copy()
            self.previous_mines_left = self.mines_left
            self.repetitions = 0
        if self.repetitions > 2 * len(self.cells_to_process) or \
           not self.cells_to_process:
            ret = False
        return ret

    def get_cells(self, row, col):
        """
        For a cell given as input get lists of all surrounding cells and their
        type.
        """
        surrounding_cells = self.get_surrounding_cells(row, col)
        closed_cells = self.filter_cells(surrounding_cells, '?')
        mine_cells = self.filter_cells(surrounding_cells, 'x')
        numbered_cells = list(set(surrounding_cells).difference(closed_cells))
        numbered_cells = list(set(numbered_cells).difference(mine_cells))
        return surrounding_cells, closed_cells, mine_cells, numbered_cells

    def filter_cells(self, cells, cell_type):
        """
        Return all cells of same type in given list of cells.
        """
        cells = [(row, col) for row, col in cells
                 if self.mine_field[row][col] == cell_type]
        return cells

    def get_all_open_cells(self):
        """
        Get all open cells.
        """
        num_rows = len(self.mine_field)
        num_cols = len(self.mine_field[0])
        open_cells = [(row, col)
                      for row in range(num_rows)
                      for col in range(num_cols)
                      if not self.mine_field[row][col] == '?']
        return open_cells

    def get_all_numbered_cells(self):
        """
        Get all numbered cells.
        """
        num_rows = len(self.mine_field)
        num_cols = len(self.mine_field[0])
        numbered_cells = [(row, col)
                          for row in range(num_rows)
                          for col in range(num_cols)
                          if self.mine_field[row][col] != '?' and \
                             self.mine_field[row][col] != 'x']
        return numbered_cells

    def get_all_closed_cells(self):
        """
        Get all closed cells.
        """
        num_rows = len(self.mine_field)
        num_cols = len(self.mine_field[0])
        closed_cells = [(row, col)
                        for row in range(num_rows)
                        for col in range(num_cols)
                        if self.mine_field[row][col] == '?']
        return closed_cells

    def get_surrounding_cells(self, cell_row, cell_col):
        """
        Return a list of coordinates of cells that surround a cell specified
        by row and column.
        """
        positions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                     (1, 0), (1, -1), (0, -1), (-1, -1)]
        surrounding_cells = []
        max_row = len(self.mine_field) - 1
        max_col = len(self.mine_field[0]) - 1
        for pos in positions:
            row = cell_row + pos[0]
            col = cell_col + pos[1]
            if 0 <= row <= max_row and 0 <= col <= max_col:
                surrounding_cells.append((row, col))
        return surrounding_cells

    def mark_mines(self, cells):
        """
        Mark cell as containing a mine.
        """
        for cell in cells:
            row, col = cell
            self.mine_field[row][col] = 'x'
            self.mines_left -= 1
        return

    def get_state(self):
        """
        Return state of the mine field. Used to visualise the mine filed with
        print to console.
        """
        result = []
        for row in self.mine_field:
            result.append(' '.join([str(col) for col in row]))
        return '\n'.join(result)

# ----- basic test cases -------------------------------------------------------

total_start = time.time()

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
0 ? ?
0 ? ?
""".strip()
result = """
0 1 x
0 1 1
""".strip()
print('\nbasic test 2\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == '?':
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
? ? ? ? 0 0 0
? ? ? ? 0 ? ?
? ? ? 0 0 ? ?
? ? ? 0 0 ? ?
0 ? ? ? 0 0 0
0 ? ? ? 0 0 0
0 ? ? ? 0 ? ?
0 0 0 0 0 ? ?
0 0 0 0 0 ? ?
""".strip()
result = """
1 x x 1 0 0 0
2 3 3 1 0 1 1
1 x 1 0 0 1 x
1 1 1 0 0 1 1
0 1 1 1 0 0 0
0 1 x 1 0 0 0
0 1 1 1 0 1 1
0 0 0 0 0 1 x
0 0 0 0 0 1 1
""".strip()
print('\nbasic test 3\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
""".strip()
result = """
1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
""".strip()
print('\nbasic test 4\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == '?':
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
""".strip()
print('\nbasic test 5\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == '?':
    print('Solved!')
else:
    print('Not solved!')

# ----- test cases from codewars submission attempts ---------------------------

gamemap = """
0 0 0 0
0 0 0 0
? ? 0 0
? ? ? ?
? ? ? ?
? ? ? ?
? ? 0 0
0 0 0 0
0 0 0 0
0 0 0 0
""".strip()
result = """
0 0 0 0
0 0 0 0
1 1 0 0
x 2 1 1
x 3 1 x
x 2 1 1
1 1 0 0
0 0 0 0
0 0 0 0
0 0 0 0
""".strip()
print('\ntest case 1.1\n' + gamemap)
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
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 0 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 0 0 0 0 2 x 2 1 x 1 0
1 1 1 0 0 0 0 1 1 1 0 0 0 0 1 1 2 x 1 0 0 0 0 2 x 2 1 1 1 0
1 x 1 1 1 1 0 1 x 2 1 1 0 0 1 x 2 1 1 0 0 0 0 1 1 1 0 0 0 0
1 2 2 3 x 2 0 1 1 2 x 1 0 0 1 2 2 1 0 0 0 0 0 1 1 1 0 0 1 1
0 1 x 3 x 2 0 0 0 1 1 1 0 1 2 3 x 1 0 0 0 0 0 1 x 1 0 0 1 x
0 1 1 3 3 3 2 1 1 1 1 2 1 2 x x 2 2 1 1 0 0 0 1 1 1 1 1 2 1
0 0 0 1 x x 2 x 1 1 x 2 x 2 3 3 3 2 x 1 0 1 1 1 0 0 2 x 2 0
0 1 1 2 2 2 3 2 2 1 1 2 1 1 1 x 2 x 2 1 0 1 x 1 0 0 2 x 2 0
1 2 x 1 0 1 2 x 1 0 0 0 1 1 2 2 3 2 1 0 0 1 1 1 0 0 1 1 1 0
1 x 2 1 0 1 x 3 2 1 0 0 1 x 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 0
1 1 2 1 2 2 2 2 x 1 0 0 1 1 1 1 2 x 1 0 0 0 1 x 2 1 0 0 0 0
1 1 2 x 2 x 1 1 1 1 0 0 0 0 1 1 2 1 1 0 0 0 1 2 x 1 0 0 0 0
1 x 3 2 2 1 1 0 0 1 1 1 0 0 1 x 1 0 0 0 0 0 1 2 2 1 0 0 0 0
1 2 x 1 0 0 0 0 0 1 x 1 0 0 1 1 1 0 0 0 0 0 1 x 1 0 0 0 0 0
""".strip()
print('\ntest case 3\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ?
? ? 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? 0 ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 ? ? ? ? ? ?
0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0
""".strip()
result = """
0 0 0 1 x 1 1 x 1 0 0 0 0 0 1 1 1 0 0 1 x 3 x 3 1 2 1
1 1 0 1 1 1 1 1 1 0 0 0 0 0 1 x 1 1 1 2 1 3 x 3 x 2 x
x 2 1 1 0 0 0 0 0 0 1 1 1 0 1 1 1 1 x 1 0 2 2 3 1 3 2
1 2 x 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 1 x 2 1 2 x
0 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 2 3 x 2 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
""".strip()
print('\ntest case 4\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ?
? ? ? ? 0 0 ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? ? ? 0 0 0
""".strip()
result = """
1 2 x 1 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 1 1 1 1 x 1
1 x 2 1 0 0 0 0 0 0 0 0 1 1 1 0 0 0 1 1 1 1 x 1 1 1 1
1 2 2 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0 1 x 2 2 1 1 0 0 0
0 1 x 2 1 2 2 x 2 1 0 0 0 0 0 0 0 0 1 3 x 3 1 1 0 0 0
0 1 1 2 x 2 x 3 x 1 0 0 0 0 0 0 0 0 0 2 x 3 x 1 0 0 0
""".strip()
print('\ntest case 5\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == '?':
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
0 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? ? ?
0 ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ? 0
? ? ? ? 0 0 0 0 0 0
? ? ? 0 0 0 0 0 0 0
""".strip()
result = """
0 0 0 0 1 1 1 1 1 1
0 0 0 1 2 x 2 2 x 1
0 1 1 2 x 2 2 x 2 1
1 2 x 2 1 1 1 1 1 0
1 x 2 1 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
""".strip()
print('\ntest case 6\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
? ? ? 0 0 ? ? ? ? ? ? 0 0 ? ? ? ?
? ? ? 0 0 ? ? ? ? ? ? 0 0 ? ? ? ?
0 0 0 0 0 ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ?
0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ?
? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ?
""".strip()
result = """
1 x 1 0 0 2 x 2 1 x 1 0 0 1 x x 1
1 1 1 0 0 2 x 3 2 1 1 0 0 1 3 4 3
0 0 0 0 0 1 2 x 1 0 0 0 0 0 1 x x
0 0 0 0 0 0 1 1 1 0 0 0 0 0 1 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 0 0 0 0 1 2 x 1
1 x 1 0 0 0 0 0 0 0 0 0 0 1 x 2 1
""".strip()
print('\ntest case 7\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? 0 0 ? ?
0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0 0 ? ?
0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
0 ? ? ? 0 ? ? ? 0 0 0 0 0 ? ? ? 0 ? ? ?
0 ? ? ? 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? 0 0
0 ? ? ? 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? 0 0
0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 0 ? ? ? 0 0
0 ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0
0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0
0 ? ? ? 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? 0
? ? ? ? 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? 0
? ? 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? ?
? ? ? ? 0 0 ? ? ? ? ? 0 ? ? ? 0 0 ? ? ?
? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 0 0
0 ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? 0 ? ? ? ? 0 0 0 0
? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0
? ? ? ? ? 0 0 ? ? ? ? ? ? 0 ? ? ? ? ? ?
? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ?
? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ?
? ? ? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
""".strip()
result = """
0 1 1 2 1 1 0 0 0 1 1 2 2 2 2 x 1 0 0 0
0 1 x 2 x 1 0 0 0 1 x 3 x x 3 2 1 0 0 0
0 1 1 2 1 1 0 0 0 1 2 x 3 3 x 1 0 0 1 1
0 0 0 1 1 1 0 0 0 0 1 1 1 1 1 1 0 0 1 x
0 0 0 1 x 1 0 0 0 0 0 0 0 0 0 0 0 1 2 2
0 1 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 x 1
0 1 x 1 0 1 1 1 0 0 0 0 0 1 1 1 0 1 1 1
0 1 1 1 0 1 x 2 2 2 1 0 0 1 x 2 1 1 0 0
0 1 1 1 0 1 1 2 x x 1 0 0 1 1 2 x 1 0 0
0 1 x 1 0 0 0 1 2 2 1 0 0 0 0 2 2 2 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
0 1 1 1 0 0 0 0 0 1 1 1 0 0 0 1 2 x 1 0
0 1 x 1 0 0 0 0 0 1 x 2 1 1 0 1 3 3 2 0
1 2 1 1 0 0 0 0 0 1 1 2 x 1 0 2 x x 1 0
x 1 0 0 0 0 0 0 0 0 0 1 1 1 0 2 x 4 3 2
1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 2 x x
1 2 x 1 0 0 1 2 3 2 1 0 1 1 1 0 0 1 2 2
1 x 3 3 1 1 1 x x x 1 0 2 x 2 0 0 0 0 0
1 2 x 2 x 1 2 3 4 2 1 0 2 x 3 1 0 0 0 0
0 1 1 2 2 2 2 x 1 0 0 0 1 2 x 1 0 0 0 0
0 0 0 0 1 x 2 1 1 0 0 0 1 2 2 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0 1 x 2 1 0 0 0 0
0 0 0 0 0 0 0 1 2 2 1 0 1 2 x 1 0 0 0 0
1 1 1 1 1 0 0 1 x x 2 1 1 1 2 2 2 1 1 0
x 2 3 x 2 0 0 1 2 2 2 x 1 0 1 x 2 x 2 1
2 x 3 x 2 0 0 0 0 0 1 2 2 1 1 1 2 1 2 x
2 3 3 3 2 1 0 0 0 0 0 1 x 1 0 0 0 1 2 2
x 2 x 2 x 1 0 0 0 0 0 1 1 1 0 0 0 1 x 1
1 2 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1
""".strip()
print('\ntest case 8\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
?
""".strip()
result = """
0
""".strip()
print('\ntest case 9\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
?
""".strip()
result = """
x
""".strip()
print('\ntest case 10\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
? ? ?
? ? ?
? ? ?
""".strip()
result = """
x x x
x 8 x
x x x
""".strip()
print('\ntest case 11\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == '?':
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 3 3 2 1 0 0
0 0 1 3 x x x x 1 0 0
0 0 2 x x x x 5 2 0 0
0 0 3 x x x x x 2 0 0
0 0 3 x x x x x 2 0 0
0 0 2 x x x x 3 1 0 0
0 0 1 2 3 3 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
print('\ntest case 12\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

gamemap = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 3 3 2 1 0 0
0 0 1 3 x x x x 1 0 0
0 0 2 x x 6 x 5 2 0 0
0 0 3 x 4 4 x x 2 0 0
0 0 3 x 5 5 x x 2 0 0
0 0 2 x x x x 3 1 0 0
0 0 1 2 3 3 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
print('\ntest case 13\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
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

total_end = time.time()
print('total test time: {} seconds.'.format(total_end - total_start))
