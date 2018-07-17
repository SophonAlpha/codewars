"""
Solution for codewars mine sweeper challenge:
https://www.codewars.com/kata/mine-sweeper

Level: 1 kyu

If you haven't played Mine Sweeper before or forgot about it:
http://minesweeperonline.com
"""

import random

def solve_mine(map, n):
    mine_field = MineSweeper(map, n)
    mine_field.solve()
    solved = mine_field.get_state()
    return solved

def open(row, col):
    global arr_str
    mine_field = [row.split() for row in arr_str.split('\n')]
    try:
        num_mines = int(mine_field[row][col])
    except ValueError:
        num_mines = mine_field[row][col]
    return num_mines

class MineSweeper:
    """
    Mine sweeper solver class.
    """

    def __init__(self, field_map, num_mines):
        self.mine_field = [row.split() for row in field_map.split('\n')]
        self.cells_to_open = [] # All cells that can be opened safely
        self.opened_cells = [] # Cells that have been opened and don't need to be visited again.
        self.ref_cell = None

    def solve(self):
        self.cells_to_open = self.get_open_cells()
        self.opened_cells = []
        while self.cells_to_open:
            if self.unsolvable_cells():
                print('unsolvable cells!')
                break
            row, col = self.cells_to_open.pop(0)
            num_mines = open(row, col)
            self.save_opened_cell((row, col))
            self.mine_field[row][col] = num_mines
            surrounding_cells = self.get_surrounding_cells(row, col)
            closed_cells = self.get_cell_type(surrounding_cells, '?')
            mine_cells = self.get_cell_type(surrounding_cells, 'x')
            if num_mines == len(mine_cells):
                self.queue_cells_to_open(closed_cells)
            elif num_mines - len(closed_cells) - len(mine_cells) == 0:
                self.mark_mines(closed_cells)
            else:
                self.queue_cells_to_open([(row, col)])
            print(self.get_state(), '\n') # TODO: remove debug statement
        return

    def unsolvable_cells(self):
        if self.ref_cell in self.cells_to_open:

    def save_opened_cell(self, position):
        if not position in self.opened_cells:
            self.opened_cells.append(position)
        return
    
    def get_cell_type(self, surrounding_cells, cell_type):
        cells = [(row, col) for row, col in surrounding_cells
                 if self.mine_field[row][col] == cell_type]
        return cells

    def queue_cells_to_open(self, cells):
        for cell in cells:
            if cell in self.opened_cells:
                self.opened_cells.remove(cell)
        self.cells_to_open = self.cells_to_open + \
                             [cell for cell in cells
                                   if not cell in self.cells_to_open and \
                                      not cell in self.opened_cells]
        return

    def get_open_cells(self):
        num_rows = len(self.mine_field)
        num_cols = len(self.mine_field[0])
        open_cells = [(row, col) 
                      for row in range(num_rows) 
                      for col in range(num_cols)
                      if not self.mine_field[row][col] == '?']
        return open_cells

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

    def mark_mines(self, hidden_cells):
        for row, col in hidden_cells:
            self.mine_field[row][col] = 'x'
        return

    def get_state(self):
        arr_str = []
        for row in self.mine_field:
            arr_str.append(' '.join([str(col) for col in row]))
        return '\n'.join(arr_str)
              
            








class MineField:
    
    def __init__(self, mine_field=None):
        if mine_field is None:
            self.mine_field = self.generate_mine_field()
        else:
            self.mine_field = mine_field

    def generate_mine_field(self, dimensions=(9, 9), num_mines=10):
        """
        Generate the mine field. This function is used in case no mine field
        is given when instantiating a new MineSweeper object.
        """
        self.generate_empty_field(dimensions)
        self.add_mines(num_mines)
        self.calculate_cell_values()
        self.show(show_all=True)
        print()
        self.show()
        print()
        row = 1
        col = 4
        self.open(row, col)
        print()
        self.show()
        return

    def generate_empty_field(self, dimensions):
        """
        Generate an empty field. All cells contain 0.
        """
        rows, cols = dimensions
        self.mine_field = [[{'open': False, 'value': 0}
                            for _ in range(cols)] for _ in range(rows)]
        return

    def add_mines(self, num_mines):
        """
        Add the mines to the field. Positions are randomised.
        """
        num_rows = len(self.mine_field)
        num_cols = len(self.mine_field[0])
        positions = [(row, col) for col in range(num_cols) for row in range(num_rows)]
        for _ in range(num_mines):
            row, col = random.choice(positions)
            self.mine_field[row][col]['value'] = 'M'
            del positions[positions.index((row, col))]
        return

    def calculate_cell_values(self):
        """
        For each cell that does not contain a mine, calculate the number of
        mines in the surrounding 8 cells.
        """
        for row_index, row in enumerate(self.mine_field):
            for col_index, _ in enumerate(row):
                if not self.mine_field[row_index][col_index]['value'] == 'M':
                    surrounding_cells = self.get_surrounding_cells(row_index, col_index)
                    num_mines = [self.mine_field[row][col]['value']
                                 for row, col in surrounding_cells].count("M")
                    self.mine_field[row_index][col_index]['value'] = num_mines
        return

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

    def show(self, show_all=False):
        """
        Print the mine field to console. show_all controls whether only opened
        cells are shown. Setting this to True shows the content of all cells
        no matter whether the cell has been opened already or not (typically
        used for troubleshooting).
        """
        for row_index, row in enumerate(self.mine_field):
            row_string = ''
            for col_index, _ in enumerate(row):
                cell_status = self.mine_field[row_index][col_index]['open']
                cell_value = self.mine_field[row_index][col_index]['value']
                cell_char = str(cell_value) if show_all or cell_status else '?'
                row_string = row_string + cell_char + ' '
            print(row_string)
        return
    
    def open(self, cell_row, cell_col):
        """
        Open a cell. If the cell value is zero, meaning no mine and no mine in
        the surrounding cells, open all adjacent zero value cells.
        """
        self.mine_field[cell_row][cell_col]['open'] = True
        cell_value = self.mine_field[cell_row][cell_col]['value']
        if not self.hit_mine(cell_row, cell_col) and cell_value == 0:
            self.open_adjacent_cells(cell_row, cell_col)
        return
        
    def hit_mine(self, cell_row, cell_col):
        """
        Did we hit a mine?
        """
        return self.mine_field[cell_row][cell_col]['value'] == 'M'

    def open_adjacent_cells(self, cell_row, cell_col):
        """
        Open all empty surrounding cells. Repeat for any other empty cell
        that is discovered in this process.
        """
        cells_to_open = []
        cells_opened = []
        cells_to_open.append((cell_row, cell_col))
        while cells_to_open:
            row, col = cells_to_open.pop()
            self.mine_field[row][col]['open'] = True
            cells_opened.append((row, col))
            surrounding_cells = self.get_surrounding_cells(row, col)
            for s_row, s_col in surrounding_cells:
                if self.mine_field[row][col]['value'] == 0 and \
                   not self.mine_field[s_row][s_col]['value'] == 'M' and \
                   not (s_row, s_col) in cells_to_open and \
                   not (s_row, s_col) in cells_opened:
                    cells_to_open.append((s_row, s_col))
        return

    def get(self):
        """
        Return current state of the mine field.
        """

gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()
arr_str = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()

gamemap = """
0 ? ?
0 ? ?
""".strip()
arr_str = """
0 1 x
0 1 1
""".strip()

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
arr_str = """
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
arr_str = """
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

solve_mine(gamemap, 6)

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
arr_str = """
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


MineSweeper()
