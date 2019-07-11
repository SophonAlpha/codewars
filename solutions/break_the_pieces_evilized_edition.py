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

"""

import re
from solutions.performance import Profile

PERFORMANCE_STATS = []

DELTAS = {
    'ul': [(0, -1, ['u', 'r', 'ur', ' ']), (-1, -1, ['d', 'r', 'lr', ' ']),
           (-1, 0, ['d', 'l', 'll', ' '])],
    'ur': [(-1, 0, ['d', 'r', 'lr', ' ']), (-1, 1, ['d', 'l', 'll', ' ']),
           (0, 1, ['u', 'l', 'ul', ' '])],
    'll': [(1, 0, ['u', 'l', 'ul', ' ']), (1, -1, ['u', 'r', 'ur', ' ']),
           (0, -1, ['d', 'r', 'lr', ' '])],
    'lr': [(0, 1, ['d', 'l', 'll', ' ']), (1, 1, ['u', 'l', 'ul', ' ']),
           (1, 0, ['u', 'r', 'ur', ' '])],
    'u': [(0, -1, ['u', 'ur', ' ']), (-1, -1, ['d', 'r', 'lr', ' ']),
          (-1, 0, ['d', 'll', 'lr', ' ']), (-1, 1, ['d', 'll', 'l', ' ']),
          (0, 1, ['u', 'ul', ' '])],
    'd': [(0, 1, ['d', 'll', ' ']), (1, 1, ['u', 'ul', 'l', ' ']),
          (1, 0, ['u', 'ul', 'ur', ' ']), (1, -1, ['u', 'ur', 'r', ' ']),
          (0, -1, ['d', 'lr', ' '])],
    'r': [(-1, 0, ['r', 'lr', ' ']), (-1, 1, ['d', 'l', 'll', ' ']),
          (0, 1, ['l', 'ul', 'll', ' ']), (1, 1, ['u', 'l', 'ul', ' ']),
          (1, 0, ['r', 'ur', ' '])],
    'l': [(1, 0, ['l', 'ul', ' ']), (1, -1, ['r', 'u', 'ur', ' ']),
          (0, -1, ['r', 'ur', 'lr', ' ']), (-1, -1, ['r', 'd', 'lr', ' ']),
          (-1, 0, ['l', 'll', ' '])],
    ' ': [(-1, 0, ['d', 'll', 'lr', ' ']), (-1, 1, ['l', 'd', 'll', ' ']),
          (0, 1, ['l', 'll', 'ul', ' ']), (1, 1, ['l', 'u', 'ul', ' ']),
          (1, 0, ['u', 'ul', 'ur', ' ']), (1, -1, ['u', 'r', 'ur', ' ']),
          (0, -1, ['r', 'ur', 'lr', ' ']), (-1, -1, ['d', 'r', 'lr', ' '])],
    '#': [],
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
    shape_matrix, border = shape_to_matrix(shape_lines)
    cells_to_be_processed = shape_matrix[:]
    while cells_to_be_processed:
        cell = cells_to_be_processed[0]
        piece = get_piece(cell, cells_to_be_processed, shape_matrix, border, blank_shape_lines)
        if piece:
            piece = plus_to_lines(piece)
            piece = piece_to_lines(piece, blank_shape_lines)
            piece = trim_piece(piece)
            pieces.append(piece)
    return pieces

# @Profile(stats=PERFORMANCE_STATS)
def get_blank_shape(shape_lines):
    """
    Generate a blank shape. Used later to add extracted characters that make up
    one piece.
    """
    blank_shape_lines = [' ' * len(shape_line) for shape_line in shape_lines]
    return blank_shape_lines

# @Profile(stats=PERFORMANCE_STATS)
def shape_to_matrix(shape_lines):
    """
    Transform the shape into a data structure that can be used for the flood fill
    algorithm. Boolean status indicates whether the cell can be filled (True)
    or not (False). ' ' cells can only be filled once, as the they can
    only belong to one piece. '|' can belong to up to two pieces and '+' cells
    to up to four pieces.

    Each cell initialises with a dictionary that stores it's fill status.
    The dictionary keys have the following meanings:

    For '+' cells: ul - upper left corner, ur - upper right corner,
                   ll - lower left corner, lr - lower right corner
    For '-' cells: u - upper half, l - lower half
    For '|' cells: r - right half, l - left half
    For ' ' cells:   - center
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

def get_piece(cell, cells_to_be_processed, shape_matrix, border, blank_shape_lines):
#     cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
#                     'ul': '+', 'ur': '+', 'll': '+', 'lr': '+'}
    piece= {}
    work_q = set()
    is_a_piece = True
    work_q.add(cell)
    cells_to_be_processed.remove(cell)
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
                                    cells_to_be_processed,
                                    shape_matrix, border)
        work_q = work_q.union(neighbours)
    return piece

def add_piece(row, col, cell_type, piece):
    if (row, col) in piece.keys():
        piece[(row, col)].add(cell_type)
    else:
        piece[(row, col)] = {cell_type}
    return piece

def get_neighbours(cell, cells_to_be_processed, shape_matrix, border):
    # TODO: performance optimize, avoid the 32 loops, use sets
    row, col, direction = cell
    neighbours = set()
    for d_row, d_col, next_directions in DELTAS[direction]:
        next_row, next_col = row + d_row, col + d_col
        for next_direction in next_directions:
            next_cell = (next_row, next_col, next_direction)
            if next_cell in cells_to_be_processed:
                neighbours.add(next_cell)
                cells_to_be_processed.remove(next_cell)
            elif (next_row, next_col) in border and \
                 not (next_row, next_col, '#') in neighbours:
                neighbours.add((next_row, next_col, '#'))
    return neighbours

# @Profile(stats=PERFORMANCE_STATS)
def plus_to_lines(piece):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    plus_types = {'ul', 'ur', 'lr', 'll'}
    for row, col in piece.keys():
        cell_types = piece[(row, col)]
        if plus_types.intersection(cell_types):
            piece = should_be_line(row, col, cell_types, piece)
    return piece

# @Profile(stats=PERFORMANCE_STATS)
def should_be_line(row, col, cell_types, piece):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    # TODO: can this nested loop be optimized?
    neighbours = []
    for cell_type in cell_types:
        for d_row, d_col, new_cell_type in MAPPING[cell_type]:
            try:
                if piece[row + d_row, col + d_col] != ' ':
                    neighbours.append(new_cell_type)
            except KeyError:
                pass
    if len(neighbours) < 2:
        new_cell_type = neighbours.pop()
        piece[row, col] = {new_cell_type}
    return piece

# @Profile(stats=PERFORMANCE_STATS)
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

# @Profile(stats=PERFORMANCE_STATS)
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
    INPUT_SHAPE = """
+-------------------+--+
|                   |  |
|                   |  |
|  +----------------+  |
|  |                   |
|  |                   |
+--+-------------------+
""".strip('\n')

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

#     INPUT_SHAPE = """
# +--------+-+----------------+-+----------------+-+--------+
# |        | |                | |                | |        |
# |        ++++               | |                | |        |
# |        ++++               | |                | |        |
# |        ++++             +-+ +-+            +-+ +-+      |
# |        ++++             |     |            |     |      |
# +-----------+      +------+     +------------+     +------+
# | +--------+|      |                                      |
# +-+   +---+||      +--------------------------------------+
# |     |+-+|||                                             |
# |     || ++||                                             |
# |     |+---+|                                             |
# |     +-----+                                             |
# |        +-+                +-+                +-+        |
# |        +-+                | |                | |        |
# |    +------+               | |                | |        |
# |    |+----+|         +-----+ |                | |        |
# |    ||+--+||         |+-+    |              +-+ +-+      |
# |    |||++|||         || |  +-+              |     |      |
# ++   |||++|||      +--+| +--+    +-----------+     +------+
# ||   |||+-+||      |   |      +--+                        |
# ++   ||+---+|      +---+  +---+   +-----------------------+
# |    |+-++--+             |       |                       |
# |+---+--+|                +-+ +---+                       |
# |+-------+                  | |                           |
# |                           | |                           |
# |        +-+                | |                +-+        |
# |        +-+                +-+                +-+        |
# |                       +------+                          |
# |                       |+----+|                          |
# |                       ||+--+||                          |
# |       +----+          |||++|||                          |
# ++      |+--+|  ++--+   |||++|||      +-------------------+
# ||      ||++||  ||  |   |||+-+||      |                   |
# ++      ||++||  ++--+   ||+---+|      +------+     +------+
# |       |+--+|          |+-++--+             |     |      |
# |       +----+      +---+--+|                +-+ +-+      |
# |                   +-------+                  | |        |
# |                                              | |        |
# |        +-+                +-+                | |        |
# |        +-+                +-+                +-+        |
# |  +-----+ |    ++                                        |
# |  +-++----+    ++                                        |
# |    ++                                                   |
# |    ||                                                   |
# ++   |+-------------+                 +-------------------+
# ||   |              |                 |                   |
# ++   +---+ +--------+                 +------+     +------+
# |        | |                                 |     |      |
# |        | |                                 +-+ +-+      |
# |        | |                                   | |        |
# |        | |                                   | |        |
# |        | |                +-+                | |        |
# |        +-+                | |                | |        |
# |  +-----+ |    ++          | |                | |        |
# |  +-++----+    ++    +-----+ |                | +-----+  |
# |    ++               |+-+    |                |    +-+|  |
# |    ||               || |  +-+                +-+  | ||  |
# ++   |+---------------+| +--+    +----------+    +--+ |+--+
# ||   |                 |      +--+          +--+      |   |
# ++   +---+ +-----------+  +---+   +--------+   +---+  +---+
# |        | |              |       |        |       |      |
# |        | |              +-+ +---+        +---+ +-+      |
# |        | |                | |                | |        |
# |        | |                | |                | |        |
# |        | |                | |                | |        |
# +--------+-+----------------+-+----------------+-+--------+
# """.strip('\n')

    pieces = break_evil_pieces(INPUT_SHAPE)
    with open('break_the_pieces_evilized_edition.csv', 'w') as outfile:
        for entry in PERFORMANCE_STATS:
            outfile.write('{}, {}\n'.format(entry[0], entry[1]))
    for counter, text_piece in enumerate(pieces):
        print('\n{}.) piece:\n'.format(counter))
        print(text_piece)
    print()
