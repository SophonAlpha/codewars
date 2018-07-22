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
        self.cells_to_process = [] # All cells that can be opened safely
        self.processed_cells = [] # Cells that have been opened and don't need to be visited again.
        self.prev_cell_set = None
        self.repetitions = 0

    def solve(self):
        """
        Main solver function. Solves by using two strategies:
        I)  Deduction: Identify and open cells were it can be deducted
            from surrounding cell values that a cell is safe to open.
        II) Combination: If the deduction approach gets stuck, meaning no
            progress in opening more cells, switch to a combination approach. In this
            approach we calculate all possible combinations for the positions of
            the remaining mines in the remaining closed cells.
        """
        self.cells_to_process = self.get_open_cells()
        self.processed_cells = []
        while self.cells_to_process:
            if self.no_progress():
                self.eval_neighbour_cell_sets()
                if set(self.cells_to_process) == self.prev_cell_set:
                    # no further cell found. No single solution. Stop and return.
                    self.mine_field = ['?']
                    break 

                
#                 # Combination: switch to combination approach after the deduction
#                 # approach ran out of opening cells safely.
#                 mine_combinations = self.eval_all_combinations()
#                 if len(mine_combinations) == 1:
#                     self.mark_mines(list(mine_combinations[0]))
#                 else:
#                     # No single solution. Stop and return.
#                     self.mine_field = ['?']
#                     break

            row, col = self.cells_to_process.pop(0)
            num_mines = open(row, col)
            self.save_opened_cell((row, col))
            self.mine_field[row][col] = num_mines
            surrounding_cells = self.get_surrounding_cells(row, col)
            closed_cells = self.filter_cells(surrounding_cells, '?')
            mine_cells = self.filter_cells(surrounding_cells, 'x')
            if num_mines == len(mine_cells):
                # Deduction: all mines surrounding a cell have been found. It is
                # safe to open all surrounding closed cells.
                self.queue_cells_to_process(closed_cells)
            elif num_mines - len(closed_cells) - len(mine_cells) == 0:
                # Deduction: all closed cells contain mines. Mark them accordingly.
                self.mark_mines(closed_cells)
            else:
                # Cannot yet safely open the cell. Put it back at the end of the
                # processing queue.
                self.queue_cells_to_process([(row, col)])
        return

    def no_progress(self):
        """
        Detect if the deduction approach got stuck. This state is identified by
        observing the same cells rotating in the processing queue 'cells_to_process'
        at least two rounds.
        """
        if set(self.cells_to_process) == self.prev_cell_set:
            self.repetitions += 1
        else:
            self.prev_cell_set = set(self.cells_to_process)
            self.repetitions = 0
        ret = True if self.repetitions > len(self.cells_to_process) * 2 else False
        return ret

    def eval_neighbour_cell_sets(self):
        for row, col in self.cells_to_process:
            surrounding_cells = self.get_surrounding_cells(row, col)
            closed_cells = self.filter_cells(surrounding_cells, '?')
            mine_cells = self.filter_cells(surrounding_cells, 'x')
            numbered_cells = list(set(surrounding_cells).differnce(closed_cells))
            numbered_cells = list(set(surrounding_cells).differnce(mine_cells))            
            num_mines = open(row, col)
            mines_outstanding = num_mines - len(mine_cells)
            for n_row, n_col in numbered_cells:
                n_surrounding_cells = self.get_surrounding_cells(n_row, n_col)
                n_closed_cells = self.filter_cells(n_surrounding_cells, '?')
                n_mine_cells = self.filter_cells(n_surrounding_cells, 'x')
                n_num_mines = open(n_row, n_col)
                n_mines_outstanding = n_num_mines - len(n_mine_cells)
                if set(n_closed_cells).issubset(set(closed_cells)) and \
                   mines_outstanding < len(closed_cells) and \
                   n_mines_outstanding < len(n_closed_cells):
                    # Neighbours closed cells are completely included 
                
            

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

    def save_opened_cell(self, position):
        """
        Keep record of cells already being processed.
        """
        if not position in self.processed_cells:
            self.processed_cells.append(position)
        return

    def filter_cells(self, cells, cell_type):
        """
        Return all cells of same type in given list of cells.
        """
        cells = [(row, col) for row, col in cells
                 if self.mine_field[row][col] == cell_type]
        return cells

    def queue_cells_to_process(self, cells):
        """
        Queue cells for processing.
        """
        for cell in cells:
            if cell in self.processed_cells:
                self.processed_cells.remove(cell)
        self.cells_to_process = self.cells_to_process + \
                             [cell for cell in cells
                              if not cell in self.cells_to_process and \
                                 not cell in self.processed_cells]
        return

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
print(gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')

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
print(gamemap)
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
print(gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
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
print(gamemap)
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
print(gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
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
print(gamemap)
solution = solve_mine(gamemap, result.count('x'))
if solution == result:
    print('Solved!')
else:
    print('Not solved!')
