"""
Solution for codewars mine sweeper challenge:
https://www.codewars.com/kata/mine-sweeper

Level: 1 kyu

If you haven't played Mine Sweeper before or forgot about it:
http://minesweeperonline.com
"""

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
        Class setup
        """
        self.mine_field = [row.split() for row in field_map.split('\n')]
        self.mines_left = total_mines
        self.cells_to_process = [] # A queue of cells that can be opened safely.
        self.processed_cells = {} # Cells that have been opened.

    def solve(self):
        """
        Main solver function.
        
        mines must be in intersection:
        TODO: detect areas and the minimum number of mines in each area
        """
        self.cells_to_process = self.get_open_cells()
        while self.cells_to_process:
            row, col = self.get_next_cell()
            self.obvious_cells(row, col)
            if not self.get_closed_cells():
                # Done. All cells are open.
                break
#             if not cells_found:
#                 cells_found = self.mines_in_intersection(row, col)
            if not self.queue_progress():
                self.safe_neighbour_difference()
            if not self.queue_progress():
                self.safe_combination_difference()
            if not self.queue_progress():
                # No solution. Stop here.
                self.mine_field = ['?']
                break
        return

    def get_next_cell(self):
        """
        Get the next cell from the queue for processing.
        """
        cell = self.cells_to_process.pop(0)
        if cell in self.processed_cells.keys():
            self.processed_cells[cell] += 1
        else:
            self.processed_cells[cell] = 1
        return cell

    def queue_cells(self, cells):
        """
        Queue cells for processing.
        """
        self.cells_to_process += [cell for cell in cells
                                  if not cell in self.cells_to_process]
        return

    def queue_progress(self):
        """
        Detect if the processing queue is looping without any progress.
        """
        ret = True
        if self.cells_to_process:
            ret = None in [self.processed_cells.get(cell) 
                           for cell in self.cells_to_process]
        return ret

    def obvious_cells(self, row, col):
        """
        Implements rule:
        
        Open safe cells and mark mine cells that are obvious, meaning they can
        be deducted solely from the number of mines that surrounds the cell and
        the state of the surrounding cells. E.g. number of mines = 1 and the
        surrounding cells already contain one mine then all surrounding closed
        cells are safe to open.
        """
        # TODO: refactor opening process, common code
        num_mines = open(row, col)
#         self.save_opened_cell((row, col))
        self.mine_field[row][col] = num_mines
        _, closed_cells, mine_cells, _ = self.get_cells(row, col)
        if num_mines == len(mine_cells):
            # Safe cells deduction: all mines surrounding the cell have been 
            # found. It is safe to open all surrounding closed cells.
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

    def mines_in_intersection(self, row, col):
        """
        Implements rule:
        
        All closed cells overlapping between current and neighbouring cell
        contain mines IF the number of remaining mines for current and
        neighbouring cell are equal AND the number of overlapping closed cells
        is equal the number of remaining mines for the current or neighbouring
        cell.
        """
        cells_found = False
        num_mines = open(row, col)
        self.mine_field[row][col] = num_mines
        _, closed_cells, mine_cells, numbered_cells = self.get_cells(row, col)
        mines_outstanding = num_mines - len(mine_cells)
        for n_row, n_col in numbered_cells:
            _, n_closed_cells, n_mine_cells, _ = self.get_cells(n_row, n_col)
            n_num_mines = open(n_row, n_col)
            n_mines_outstanding = n_num_mines - len(n_mine_cells)
            overlap = list(set(closed_cells) & set(n_closed_cells))
            if mines_outstanding == n_mines_outstanding and \
               len(overlap) == mines_outstanding:
                # Overlapping closed cells are all mines.
                self.mark_mines(overlap)
                cells_found = True
        return cells_found

    def safe_neighbour_difference(self):
        """
        Implements rule:
        
        The difference between closed cells of the current cell and a neighbour
        cell are safe cells IF number of remaining mines (must be > 0) are equal
        between current and neighbour AND neighbour closed cells are a 
        strict subset of current cell closed cells.
        """
        safe_cells = []
        for row, col in self.cells_to_process:
            _, closed_cells, mine_cells, numbered_cells = self.get_cells(row, col)
            num_mines = open(row, col)
            mines_outstanding = num_mines - len(mine_cells)
            diff_cells = []
            for n_row, n_col in numbered_cells:
                _, n_closed_cells, n_mine_cells, _ = self.get_cells(n_row, n_col)
                n_num_mines = open(n_row, n_col)
                n_mines_outstanding = n_num_mines - len(n_mine_cells)
                if n_closed_cells and \
                   mines_outstanding > 0 and \
                   set(n_closed_cells).issubset(set(closed_cells)) and \
                   n_mines_outstanding == mines_outstanding:
                    # The neighbour cell's closed cells are completely included
                    diff_cells = diff_cells + n_closed_cells
            if diff_cells:
                safe_cells = safe_cells + \
                             list(set(closed_cells).difference(set(diff_cells)))
        self.queue_cells(safe_cells)
        return

    def safe_combination_difference(self):
        """
        rule:
        """
        mine_combinations = self.eval_all_combinations()
        combination_cells = [cell for combination in mine_combinations
                             for cell in combination]
        safe_cells = set(self.get_closed_cells()) - set(combination_cells)
        self.queue_cells(safe_cells)
        return
    
    def get_cells(self, row, col):
        """
        For a cell given as input get lists of all cell types.
        """
        surrounding_cells = self.get_surrounding_cells(row, col)
        closed_cells = self.filter_cells(surrounding_cells, '?')
        mine_cells = self.filter_cells(surrounding_cells, 'x')
        numbered_cells = list(set(surrounding_cells).difference(closed_cells))
        numbered_cells = list(set(numbered_cells).difference(mine_cells))
        return surrounding_cells, closed_cells, mine_cells, numbered_cells

    def eval_all_combinations(self):
        """
        Test all combinations of remaining mines in the remaining closed cells.
        Return all possible solutions.
        """
        mine_combinations = []
        all_closed_cells = self.get_closed_cells()
        combinations = list(itertools.combinations(all_closed_cells,
                                                   r=self.mines_left))
        for combination in combinations:
            combination_fit = False
            for row, col in self.cells_to_process:
                surrounding_cells = self.get_surrounding_cells(row, col)
                closed_cells = self.filter_cells(surrounding_cells, '?')
                mine_cells = self.filter_cells(surrounding_cells, 'x')
                num_mines = open(row, col)
                remaining_mines = num_mines - len(mine_cells)
                possible_cells = set(combination) & set(closed_cells)
                if len(possible_cells) == remaining_mines:
                    combination_fit = True
                else:
                    combination_fit = False
                    break
            if combination_fit:
                mine_combinations.append(combination)
        return mine_combinations

    def filter_cells(self, cells, cell_type):
        """
        Return all cells of same type in given list of cells.
        """
        cells = [(row, col) for row, col in cells
                 if self.mine_field[row][col] == cell_type]
        return cells

    def get_open_cells(self):
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
    
    def get_closed_cells(self):
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
        Mark cells as containing a mine.
        """
        for row, col in cells:
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
print('\ntest case 3\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')


import sys
sys.exit("Stop here for now.")


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
print('\ntest case 1\n' + gamemap)
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
print('\ntest case 2\n' + gamemap)
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
print('\ntest case 2.1\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
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
print('\ntest case 4\n' + gamemap)
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
print('\ntest case 5\n' + gamemap)
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
print('\ntest case 6\n' + gamemap)
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
print('\ntest case 7\n' + gamemap)
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
print('\ntest case 8\n' + gamemap)
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
print('\ntest case 9\n' + gamemap)
solution = solve_mine(gamemap, original_map.count('x'))
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
print('\ntest case 10\n' + gamemap)
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
print('\ntest case 11\n' + gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')
