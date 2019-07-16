"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu

Performance optimizations:

    reference shape size: 67 rows, 59 columns

    2019-06-29
        approach "2x2 sub-cells",
        runtime: 10.93s

        approach "2x2 sub-cells, process white spaces",
        runtime: 11.33s

    2019-07-12
        approach "original shape (no sub-cells), traverse via dictionary",
        runtime: 8.44s

    2019-07-14
        approach "build neighbours for each cell and set intersection",
        runtime: 2.33s

    2019-07-15
        approach "replace loops with set operations in get_neighbours()",
        runtime: 0.57s
"""

import re
from solutions.performance import Profile

PERFORMANCE_STATS = []

VALID_NEIGHBOURS = {
    'ul': {(0, -1, '#'), (-1, -1, 'd'), (-1, -1, 'r'), (-1, 0, 'l'),
           (-1, 0, '#'), (-1, 0, 'd'), (-1, -1, ' '), (-1, -1, 'lr'),
           (-1, -1, '#'), (0, -1, 'u'), (-1, 0, ' '), (0, -1, ' '),
           (-1, 0, 'll'), (0, -1, 'ur'), (0, -1, 'r')},
    'ur': {(-1, 1, ' '), (-1, 1, '#'), (-1, 1, 'd'), (-1, 1, 'll'),
           (0, 1, '#'), (-1, 0, '#'), (-1, 0, 'lr'), (-1, 0, 'd'),
           (0, 1, 'l'), (-1, 1, 'l'), (0, 1, 'ul'), (-1, 0, ' '),
           (0, 1, ' '), (0, 1, 'u'), (-1, 0, 'r')},
    'll': {(1, 0, 'ul'), (0, -1, 'lr'), (0, -1, '#'), (1, 0, ' '),
           (1, 0, 'u'), (1, -1, '#'), (1, -1, ' '), (0, -1, 'd'),
           (1, -1, 'ur'), (1, -1, 'r'), (0, -1, ' '), (1, 0, '#'),
           (1, 0, 'l'), (1, -1, 'u'), (0, -1, 'r')},
    'lr': {(1, 1, ' '), (1, 1, '#'), (1, 0, 'r'), (1, 0, 'ur'), (1, 0, ' '),
           (0, 1, '#'), (0, 1, 'l'), (1, 0, 'u'), (0, 1, 'll'), (1, 1, 'l'),
           (1, 1, 'u'), (1, 0, '#'), (0, 1, ' '), (0, 1, 'd'), (1, 1, 'ul')},
    'u': {(-1, 1, ' '), (0, -1, '#'), (-1, -1, 'd'), (-1, 1, 'll'),
          (0, 1, '#'), (-1, 0, 'lr'), (-1, 0, 'd'), (-1, -1, ' '),
          (-1, -1, 'lr'), (0, -1, 'u'), (0, 1, 'ul'), (-1, 0, ' '),
          (0, 1, ' '), (-1, 1, '#'), (-1, 1, 'd'), (-1, -1, 'r'),
          (-1, 0, '#'), (-1, -1, '#'), (-1, 1, 'l'), (0, -1, ' '),
          (0, -1, 'ur'), (-1, 0, 'll'), (0, 1, 'u')},
    'd': {(1, 1, ' '), (0, -1, '#'), (0, 1, '#'), (1, 0, 'u'), (0, 1, 'll'),
          (1, -1, ' '), (1, 1, 'l'), (1, -1, 'ur'), (1, 1, 'u'), (1, 0, '#'),
          (0, 1, ' '), (1, 1, '#'), (1, 0, 'ul'), (1, 0, 'ur'), (0, -1, 'lr'),
          (1, 0, ' '), (1, -1, '#'), (0, -1, 'd'), (1, -1, 'r'), (0, -1, ' '),
          (1, -1, 'u'), (0, 1, 'd'), (1, 1, 'ul')},
    'r': {(-1, 1, ' '), (1, 1, ' '), (1, 0, 'r'), (-1, 1, 'll'), (0, 1, '#'),
          (-1, 0, 'lr'), (0, 1, 'll'), (1, 1, 'l'), (0, 1, 'ul'), (1, 1, 'u'),
          (1, 0, '#'), (-1, 0, ' '), (0, 1, ' '), (-1, 1, '#'), (1, 1, '#'),
          (1, 0, 'ur'), (-1, 1, 'd'), (1, 0, ' '), (-1, 0, '#'), (0, 1, 'l'),
          (-1, 1, 'l'), (1, 1, 'ul'), (-1, 0, 'r')},
    'l': {(0, -1, '#'), (-1, -1, 'd'), (-1, 0, 'l'), (1, -1, ' '),
          (-1, -1, ' '), (-1, -1, 'lr'), (1, -1, 'ur'), (1, 0, '#'),
          (-1, 0, ' '), (0, -1, 'r'), (1, 0, 'ul'), (0, -1, 'lr'), (1, 0, ' '),
          (-1, -1, 'r'), (-1, 0, '#'), (1, -1, '#'), (1, -1, 'u'),
          (-1, -1, '#'), (1, -1, 'r'), (0, -1, ' '), (1, 0, 'l'),
          (0, -1, 'ur'), (-1, 0, 'll')},
    ' ': {(0, -1, '#'), (-1, 0, 'lr'), (1, 0, 'u'), (-1, 0, 'd'),
          (-1, -1, 'lr'), (1, 1, 'l'), (1, 1, 'u'), (0, 1, ' '), (0, -1, 'r'),
          (-1, 1, '#'), (1, 1, '#'), (1, 0, 'ur'), (0, -1, 'lr'), (1, 0, ' '),
          (-1, -1, 'r'), (0, 1, 'l'), (1, -1, '#'), (-1, 1, 'l'),
          (-1, -1, '#'), (1, -1, 'r'), (0, -1, 'ur'), (1, 1, 'ul'),
          (-1, 1, ' '), (1, 1, ' '), (-1, 1, 'll'), (-1, -1, 'd'), (0, 1, '#'),
          (0, 1, 'll'), (1, -1, ' '), (-1, -1, ' '), (1, -1, 'ur'),
          (0, 1, 'ul'), (1, 0, '#'), (-1, 0, ' '), (1, 0, 'ul'), (-1, 1, 'd'),
          (-1, 0, '#'), (0, -1, ' '), (1, -1, 'u'), (-1, 0, 'll')},
    '#': set(),
    }

@Profile(stats=PERFORMANCE_STATS)
def break_evil_pieces(shape):
    """
    main function

    Extract individual pieces from shape and return in list.
    """
    pieces = []
    shape_lines = shape.split('\n')
    blank_shape_lines = get_blank_shape(shape_lines)
    shape_cell_q, shape_cells, shape_inside = pre_process(shape_lines)
    shape_neighbour_map = get_neighbour_map(shape_cells)
    while shape_cell_q:
        cell = shape_cell_q.pop()
        piece, shape_cell_q = get_piece(cell, shape_cell_q,
                                        shape_neighbour_map, shape_inside)
        if piece:
            piece = plus_to_lines(piece)
            piece = piece_to_lines(piece, blank_shape_lines)
            piece = trim_piece(piece)
            pieces.append(piece)
    return pieces

@Profile(stats=PERFORMANCE_STATS)
def get_blank_shape(shape_lines):
    """
    Generate a blank shape. Used later to add extracted characters that make up
    one piece.
    """
    blank_shape_lines = [' ' * len(shape_line) for shape_line in shape_lines]
    return blank_shape_lines

@Profile(stats=PERFORMANCE_STATS)
def pre_process(shape_lines):
    """
    Transform the shape into several data structures that will be used for
    extracting individual pieces.

    shape_cell_q - a queue filled with all the cells that need to be evaluated
    shape_cells  - a dictionary that allows to address indiviual cells by
                   row, column
    shape_inside - all cells of the shape. This is used to detect whether a
                   row, column tuple is outside the shape (at the border).
                   It indicates that a set of cells is a border element and not
                   a valid piece.
    """
    cell_types = {'+': ['ul', 'ur', 'll', 'lr'],
                  '-': ['u', 'd'],
                  '|': ['r', 'l'],
                  ' ': [' '],}
    shape_cell_q = set()
    shape_cells = {}
    for row, shape_line in enumerate(shape_lines):
        for col, cell in enumerate(shape_line):
            for direction in cell_types[cell]:
                shape_cell_q.add((row, col, direction))
            shape_cells[(row, col)] = cell_types[cell]
    shape_inside = shape_cell_q.copy()
    return shape_cell_q, shape_cells, shape_inside

@Profile(stats=PERFORMANCE_STATS)
def get_neighbour_map(shape_cells):
    """
    Build a dictionary data structure where for each cell (a row, column tuple)
    all neighbouring cells are returned.
    """
    deltas = [(-1, 0), (-1, 1), (0, 1), (1, 1),
              (1, 0), (1, -1), (0, -1), (-1, -1),]
    shape_neighbour_map = {}
    for row, col in shape_cells:
        neighbour_cells = set()
        for d_row, d_col in deltas:
            n_row, n_col = row + d_row, col + d_col
            if (n_row, n_col) in shape_cells.keys():
                new_set = {(d_row, d_col, cell)
                           for cell in shape_cells[(n_row, n_col)]}
                neighbour_cells = neighbour_cells.union(new_set)
            else:
                neighbour_cells.add((d_row, d_col, '#'))
        shape_neighbour_map[(row, col)] = neighbour_cells
    return shape_neighbour_map

@Profile(stats=PERFORMANCE_STATS)
def get_piece(cell, shape_cell_q, shape_neighbour_map, shape_inside):
    """
    Extract a single piece.
    """
    piece = {}
    is_a_piece = True
    work_q = set()
    work_q.add(cell)
    while work_q:
        cell, work_q, is_a_piece, piece = get_cell(work_q, is_a_piece, piece)
#         cell = work_q.pop()
#         _, _, cell_type = cell
#         if cell_type == '#' and is_a_piece:
#             is_a_piece = False
#             piece = None
#         if is_a_piece:
#             piece = add_cell(cell, piece)
        shape_cell_q, neighbours = get_neighbours(cell, shape_cell_q,
                                                  shape_neighbour_map,
                                                  shape_inside)
        work_q = update_work_queue(work_q, neighbours)
#         work_q = work_q.union(neighbours)
    return piece, shape_cell_q

@Profile(stats=PERFORMANCE_STATS)
def get_cell(work_q, is_a_piece, piece):
    cell = work_q.pop()
    _, _, cell_type = cell
    if cell_type == '#' and is_a_piece:
        is_a_piece = False
        piece = None
    if is_a_piece:
        piece = add_cell(cell, piece)
    return cell, work_q, is_a_piece, piece

@Profile(stats=PERFORMANCE_STATS)
def update_work_queue(work_q, neighbours):
    work_q = work_q.union(neighbours)
    return work_q

@Profile(stats=PERFORMANCE_STATS)
def add_cell(cell, piece):
    """
    Add a single cell to the current piece.
    """
    row, col, cell_type = cell
    if (row, col) in piece.keys():
        piece[(row, col)].add(cell_type)
    else:
        piece[(row, col)] = {cell_type}
    return piece

@Profile(stats=PERFORMANCE_STATS)
def get_neighbours(cell, shape_cell_q, shape_neighbour_map, shape_inside):
    """
    For a given cell extract all valid neighbour and border cells. This is done
    via set operations for significantly higher performance compared to operating
    on lists.
    """
    neighbours = set()
    row, col, cell_type = cell
    if cell_type != '#':
        next_cells = VALID_NEIGHBOURS[cell_type].intersection(shape_neighbour_map[(row, col)])
        next_cells = get_absolut_positions(cell, next_cells)
        neighbours = shape_cell_q.intersection(next_cells)
        shape_cell_q = shape_cell_q.difference(neighbours)
        neighbours = neighbours.union(next_cells.difference(shape_inside))
    return shape_cell_q, neighbours

@Profile(stats=PERFORMANCE_STATS)
def get_absolut_positions(cell, neighbours):
    """
    Transform relative row, column coordinates into absolute coordinates.
    """
    row, col, _ = cell
    neighbours = {(row + d_row, col + d_col, cell_type)
                  for d_row, d_col, cell_type in neighbours}
    return neighbours

@Profile(stats=PERFORMANCE_STATS)
def plus_to_lines(piece):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    plus_types = {'ul', 'ur', 'lr', 'll'}
    for row, col in piece.keys():
        if plus_types.intersection(piece[(row, col)]):
            piece = should_be_line(row, col, piece)
    return piece

@Profile(stats=PERFORMANCE_STATS)
def should_be_line(row, col, piece):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    if piece[row, col] == {'ul', 'ur'} and \
       piece[row - 1, col].intersection({' ', 'd'}):
        piece[row, col] = {'u'}
    elif piece[row, col] == {'ll', 'lr'} and \
         piece[row + 1, col].intersection({' ', 'u'}):
        piece[row, col] = {'d'}
    elif piece[row, col] == {'ul', 'll'} and \
         piece[row, col - 1].intersection({' ', 'r'}):
        piece[row, col] = {'l'}
    elif piece[row, col] == {'ur', 'lr'} and \
         piece[row, col + 1].intersection({' ', 'l'}):
        piece[row, col] = {'r'}
    return piece

@Profile(stats=PERFORMANCE_STATS)
def piece_to_lines(piece, blank_shape_lines):
    """
    Transform the piece matrix into a list of text lines.
    """
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+'}
    shape = blank_shape_lines[:]
    for row, col in piece.keys():
        cell = piece[(row, col)].pop()
        shape[row] = shape[row][:col] + cell_to_char[cell] + shape[row][col + 1:]
    return shape

@Profile(stats=PERFORMANCE_STATS)
def trim_piece(shape):
    """
    Remove all unnecessary white space around an extracted piece.
    """
    min_start = None
    pattern = re.compile(r'(^ *)(?P<shape>.*?)( *)$')
    for row in shape:
        match = pattern.fullmatch(row)
        if match.group('shape'):
            start = match.start('shape')
            min_start = start if min_start is None or min_start > start else min_start
    shape_new = []
    for row in shape:
        if row.strip():
            shape_new.append(row[min_start:].rstrip())
    shape_new = '\n'.join(shape_new)
    return shape_new

if __name__ == '__main__':
#     INPUT_SHAPE = """
#     +------+
#     |+----+|
#     ||+--+||
#     |||++|||
#     |||++|||
#     |||+-+||
#     ||+---+|
#     |+-++--+
# +---+--+|
# +-------+
# """.strip('\n')

    INPUT_SHAPE = """
+--------+-+----------------+-+----------------+-+--------+
|        | |                | |                | |        |
|        ++++               | |                | |        |
|        ++++               | |                | |        |
|        ++++             +-+ +-+            +-+ +-+      |
|        ++++             |     |            |     |      |
+-----------+      +------+     +------------+     +------+
| +--------+|      |                                      |
+-+   +---+||      +--------------------------------------+
|     |+-+|||                                             |
|     || ++||                                             |
|     |+---+|                                             |
|     +-----+                                             |
|        +-+                +-+                +-+        |
|        +-+                | |                | |        |
|    +------+               | |                | |        |
|    |+----+|         +-----+ |                | |        |
|    ||+--+||         |+-+    |              +-+ +-+      |
|    |||++|||         || |  +-+              |     |      |
++   |||++|||      +--+| +--+    +-----------+     +------+
||   |||+-+||      |   |      +--+                        |
++   ||+---+|      +---+  +---+   +-----------------------+
|    |+-++--+             |       |                       |
|+---+--+|                +-+ +---+                       |
|+-------+                  | |                           |
|                           | |                           |
|        +-+                | |                +-+        |
|        +-+                +-+                +-+        |
|                       +------+                          |
|                       |+----+|                          |
|                       ||+--+||                          |
|       +----+          |||++|||                          |
++      |+--+|  ++--+   |||++|||      +-------------------+
||      ||++||  ||  |   |||+-+||      |                   |
++      ||++||  ++--+   ||+---+|      +------+     +------+
|       |+--+|          |+-++--+             |     |      |
|       +----+      +---+--+|                +-+ +-+      |
|                   +-------+                  | |        |
|                                              | |        |
|        +-+                +-+                | |        |
|        +-+                +-+                +-+        |
|  +-----+ |    ++                                        |
|  +-++----+    ++                                        |
|    ++                                                   |
|    ||                                                   |
++   |+-------------+                 +-------------------+
||   |              |                 |                   |
++   +---+ +--------+                 +------+     +------+
|        | |                                 |     |      |
|        | |                                 +-+ +-+      |
|        | |                                   | |        |
|        | |                                   | |        |
|        | |                +-+                | |        |
|        +-+                | |                | |        |
|  +-----+ |    ++          | |                | |        |
|  +-++----+    ++    +-----+ |                | +-----+  |
|    ++               |+-+    |                |    +-+|  |
|    ||               || |  +-+                +-+  | ||  |
++   |+---------------+| +--+    +----------+    +--+ |+--+
||   |                 |      +--+          +--+      |   |
++   +---+ +-----------+  +---+   +--------+   +---+  +---+
|        | |              |       |        |       |      |
|        | |              +-+ +---+        +---+ +-+      |
|        | |                | |                | |        |
|        | |                | |                | |        |
|        | |                | |                | |        |
+--------+-+----------------+-+----------------+-+--------+
""".strip('\n')

    ALL_PIECES = break_evil_pieces(INPUT_SHAPE)
    with open('break_the_pieces_evilized_edition.csv', 'w') as outfile:
        outfile.write('{}; {}; {}\n'.format('function', 'time', 'arguments'))
        for entry in PERFORMANCE_STATS:
            outfile.write('{}; {}; {}\n'.format(entry[0], entry[1], entry[2]))
    for counter, text_piece in enumerate(ALL_PIECES):
        print('\n{}.) piece:\n'.format(counter))
        print(text_piece)
    print()
