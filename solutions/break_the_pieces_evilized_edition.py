"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu

Performance optimizations:

    reference shape size: 67 rows, 59 columns
    
    2019-06-29 
        approach "2x2 sub-cells", runtime: 10.93s
        shape shape_matrix size: 15812
        work q loops: 15812
        direction loops: 58324
    
        approach "2x2 sub-cells, process white spaces", runtime: 11.33s
        shape shape_matrix size: 15812
        work q loops: 9615
        direction loops: 33536

    2019-07-12
        approach "original shape, traverse via dictionary", runtime: 8.44s
        
    2019-07-14
        approach "build neighbours for each cell and set intersection",
        runtime: 2.33s

"""

import re
from solutions.performance import Profile

PERFORMANCE_STATS = []

# VALID_NEIGHBOURS = {
#     'ul': [(0, -1, ['u', 'r', 'ur', ' ', '#']), (-1, -1, ['d', 'r', 'lr', ' ', '#']),
#            (-1, 0, ['d', 'l', 'll', ' ', '#'])],
#     'ur': [(-1, 0, ['d', 'r', 'lr', ' ', '#']), (-1, 1, ['d', 'l', 'll', ' ', '#']),
#            (0, 1, ['u', 'l', 'ul', ' ', '#'])],
#     'll': [(1, 0, ['u', 'l', 'ul', ' ', '#']), (1, -1, ['u', 'r', 'ur', ' ', '#']),
#            (0, -1, ['d', 'r', 'lr', ' ', '#'])],
#     'lr': [(0, 1, ['d', 'l', 'll', ' ', '#']), (1, 1, ['u', 'l', 'ul', ' ', '#']),
#            (1, 0, ['u', 'r', 'ur', ' ', '#'])],
#     'u': [(0, -1, ['u', 'ur', ' ', '#']), (-1, -1, ['d', 'r', 'lr', ' ', '#']),
#           (-1, 0, ['d', 'll', 'lr', ' ', '#']), (-1, 1, ['d', 'll', 'l', ' ', '#']),
#           (0, 1, ['u', 'ul', ' ', '#'])],
#     'd': [(0, 1, ['d', 'll', ' ', '#']), (1, 1, ['u', 'ul', 'l', ' ', '#']),
#           (1, 0, ['u', 'ul', 'ur', ' ', '#']), (1, -1, ['u', 'ur', 'r', ' ', '#']),
#           (0, -1, ['d', 'lr', ' ', '#'])],
#     'r': [(-1, 0, ['r', 'lr', ' ', '#']), (-1, 1, ['d', 'l', 'll', ' ', '#']),
#           (0, 1, ['l', 'ul', 'll', ' ', '#']), (1, 1, ['u', 'l', 'ul', ' ', '#']),
#           (1, 0, ['r', 'ur', ' ', '#'])],
#     'l': [(1, 0, ['l', 'ul', ' ', '#']), (1, -1, ['r', 'u', 'ur', ' ', '#']),
#           (0, -1, ['r', 'ur', 'lr', ' ', '#']), (-1, -1, ['r', 'd', 'lr', ' ', '#']),
#           (-1, 0, ['l', 'll', ' ', '#'])],
#     ' ': [(-1, 0, ['d', 'll', 'lr', ' ', '#']), (-1, 1, ['l', 'd', 'll', ' ', '#']),
#           (0, 1, ['l', 'll', 'ul', ' ', '#']), (1, 1, ['l', 'u', 'ul', ' ', '#']),
#           (1, 0, ['u', 'ul', 'ur', ' ', '#']), (1, -1, ['u', 'r', 'ur', ' ', '#']),
#           (0, -1, ['r', 'ur', 'lr', ' ', '#']), (-1, -1, ['d', 'r', 'lr', ' ', '#'])],
#     '#': [],
#     }
#  
# NEW_DELTAS = {}
# for dir_ in VALID_NEIGHBOURS:
#     new_set = set()
#     for (row, col, cell_dirs) in VALID_NEIGHBOURS[dir_]:
#         new_set = new_set.union({(row, col, cell_dir)
#                                  for cell_dir in cell_dirs})
#     NEW_DELTAS[dir_] = new_set

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


MAPPING = {
    'ul': [(-1, 0, 'l'), (0, -1, 'u')],
    'ur': [(-1, 0, 'r'), (0, 1, 'u')],
    'lr': [(0, 1, 'd'), (1, 0, 'r')],
    'll': [(1, 0, 'l'), (0, -1, 'd')],
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
    shape_cell_q, shape_cells, shape_border = pre_process(shape_lines)
    shape_neighbour_map = get_neighbour_map(shape_cells, shape_border)
    while shape_cell_q:
        cell = shape_cell_q[0]
        piece = get_piece(cell, shape_cell_q, shape_neighbour_map, shape_border)
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
    Transform the shape into a data structure that can be used for the flood fill
    algorithm.
    """
    cell_types = {'+': ['ul', 'ur', 'll', 'lr'],
                  '-': ['u', 'd'],
                  '|': ['r', 'l'],
                  ' ': [' '],}
    shape_cell_q = []
    shape_cells = {}
    shape_border = set()
    shape_border = add_top_border(shape_border, shape_lines)
    for row, shape_line in enumerate(shape_lines):
        shape_border = add_right_left_border(shape_border, row, shape_line)
        for col, cell in enumerate(shape_line):
            for direction in cell_types[cell]:
                shape_cell_q.append((row, col, direction))
            shape_cells[(row, col)] =  cell_types[cell]
    shape_border = add_bottom_border(shape_border, shape_lines)
    return shape_cell_q, shape_cells, shape_border

@Profile(stats=PERFORMANCE_STATS)
def get_neighbour_map(shape_cells, shape_border):
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
            if (n_row, n_col) in shape_border:
                neighbour_cells.add((d_row, d_col, '#'))
        shape_neighbour_map[(row, col)] = neighbour_cells
    return shape_neighbour_map

@Profile(stats=PERFORMANCE_STATS)
def add_top_border(shape_border, shape_lines):
    for elem in range(len(shape_lines[0]) + 2):
        shape_border.add((-1, elem - 1))
    return shape_border

@Profile(stats=PERFORMANCE_STATS)
def add_right_left_border(shape_border, row, shape_line):
    shape_border.add((row, -1))
    shape_border.add((row, len(shape_line)))
    return shape_border

@Profile(stats=PERFORMANCE_STATS)
def add_bottom_border(shape_border, shape_lines):
    for elem in range(len(shape_lines[-1]) + 2):
        shape_border.add((len(shape_lines), elem - 1))    
    return shape_border

@Profile(stats=PERFORMANCE_STATS)
def shape_to_matrix_v1(shape_lines):
    """
    Transform the shape into a data structure that can be used for the flood fill
    algorithm.
    """
    directions = {'+': ['ul', 'ur', 'll', 'lr'],
                  '-': ['u', 'd'],
                  '|': ['r', 'l'],
                  ' ': [' '],}
    shape_matrix = []
    border = set()
    for elem in range(len(shape_lines[0]) + 2):
        border.add((-1, elem - 1))
    for row, shape_line in enumerate(shape_lines):
        border.add((row, -1))
        border.add((row, len(shape_line)))
        for col, cell in enumerate(shape_line):
            for direction in directions[cell]:
                shape_matrix.append((row, col, direction))
    for elem in range(len(shape_lines[-1]) + 2):
        border.add((len(shape_lines), elem - 1))
    return shape_matrix, border

@Profile(stats=PERFORMANCE_STATS)
def get_piece(cell, shape_cell_q, shape_neighbour_map, shape_border):
    piece= {}
    work_q = set()
    is_a_piece = True
    work_q.add(cell)
    shape_cell_q.remove(cell)
    while work_q:
        # TODO: performance optimize, around half of the sourrounding cells 
        #       already in queue, avoid testing, maybe using sets helps
        row, col, cell_type = work_q.pop()
        if cell_type == '#':
            is_a_piece = False
            piece = None
        if is_a_piece:
            piece = add_piece(row, col, cell_type, piece)
        neighbours = get_neighbours((row, col, cell_type),
                                    shape_cell_q, shape_neighbour_map,
                                    shape_border)
        work_q = work_q.union(neighbours)
    return piece

@Profile(stats=PERFORMANCE_STATS)
def add_piece(row, col, cell_type, piece):
    if (row, col) in piece.keys():
        piece[(row, col)].add(cell_type)
    else:
        piece[(row, col)] = {cell_type}
    return piece

@Profile(stats=PERFORMANCE_STATS)
def get_neighbours(cell, shape_cell_q, shape_neighbour_map, shape_border):
    neighbours = []
    row, col, cell_type = cell
    if cell_type != '#':
        next_cells = VALID_NEIGHBOURS[cell_type].intersection(shape_neighbour_map[(row, col)])
        next_cells = get_absolut_positions(cell, next_cells)
        for next_cell in next_cells:
            next_row, next_col, _ = next_cell
            if next_cell in shape_cell_q:
                neighbours.append(next_cell)
                shape_cell_q.remove(next_cell)
            elif (next_row, next_col) in shape_border:
                neighbours.append(next_cell)
    return neighbours

@Profile(stats=PERFORMANCE_STATS)
def get_absolut_positions(cell, neighbours):
    row, col, _ = cell
    neighbours = [(row + d_row, col + d_col, cell_type)
                  for d_row, d_col, cell_type in neighbours]
    return neighbours

@Profile(stats=PERFORMANCE_STATS)
def plus_to_lines(piece):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    plus_types = {'ul', 'ur', 'lr', 'll'}
    for row, col in piece.keys():
        cell_types = piece[(row, col)]
        if plus_types.intersection(cell_types):
            piece = should_be_line(row, col, piece)
    return piece

@Profile(stats=PERFORMANCE_STATS)
def should_be_line(row, col, piece):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    if piece[row, col] == {'ul', 'ur'} and \
       piece[row - 1, col].issubset({' ', 'd'}):
        piece[row, col] = {'u'}
    elif piece[row, col] == {'ll', 'lr'} and \
         piece[row + 1, col].issubset({' ', 'u'}):
        piece[row, col] = {'d'}
    elif piece[row, col] == {'ul', 'll'} and \
         piece[row, col - 1].issubset({' ', 'r'}):
        piece[row, col] = {'l'}
    elif piece[row, col] == {'ur', 'lr'} and \
         piece[row, col + 1].issubset({' ', 'l'}):
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
# +----------+
# |          |
# |          |
# |          |
# +----------+
# |          |
# |          |
# +----------+
# """.strip('\n')

#     INPUT_SHAPE = """
#           
#  +---+-+ 
#  |   | | 
#  | +-+ | 
#  | |   | 
#  | +---+ 
#  |     | 
#  +-----+ 
#           
# """.strip('\n')

#     INPUT_SHAPE = """
# +----+---+
# |    |   |
# | +--+   |
# | |      |
# | +------+
# |        |
# +--------+
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

    pieces = break_evil_pieces(INPUT_SHAPE)
    with open('break_the_pieces_evilized_edition.csv', 'w') as outfile:
        for entry in PERFORMANCE_STATS:
            outfile.write('{}, {}\n'.format(entry[0], entry[1]))
    for counter, text_piece in enumerate(pieces):
        print('\n{}.) piece:\n'.format(counter))
        print(text_piece)
    print()
