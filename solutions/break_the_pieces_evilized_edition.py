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
import time

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

# @Profile(stats=PERFORMANCE_STATS)
def break_evil_pieces(shape):
    """
    main function

    Extract individual pieces from shape and return in list.
    """
    txt_pieces = []
    shape_lines = shape.split('\n')
    blank_shape_lines = get_blank_shape(shape_lines)
    shape_cell_q, shape_cells, shape_inside, shape_space_cells, shape_border_cells = pre_process(shape_lines)
    shape_neighbour_map = get_neighbour_map(shape_cells)
    # TODO: white pieces and borders to classes
    shape_white_pieces, shape_cell_to_white_piece_map = get_white_piece_map(shape_neighbour_map,
                                                                            shape_inside,
                                                                            shape_space_cells)
    pieces = get_pieces(shape_neighbour_map,
                        shape_inside,
                        shape_space_cells,
                        shape_border_cells,
                        shape_white_pieces,
                        shape_cell_to_white_piece_map)
    for idx in pieces:
        piece = pieces[idx]
        piece = set_to_dict(piece)
        piece = plus_to_lines(piece)
        piece = piece_to_lines(piece, blank_shape_lines)
        piece = trim_piece(piece)
        txt_pieces.append(piece)
    return txt_pieces

def DEBUG_display_white_piece_map(shape_white_pieces, shape_cells, blank_shape_lines):
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+',
                    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                    '6': '6', '7': '7', '8': '8', '9': '9',}
    shape = blank_shape_lines[:]
    for idx in shape_white_pieces:
        for row, col, _ in shape_white_pieces[idx]:
            shape_cells[(row, col)] = ['{}'.format(idx % 9)]
    for row, col in shape_cells.keys():
        cell = shape_cells[(row, col)][0]
        shape[row] = shape[row][:col] + cell_to_char[cell] + shape[row][col + 1:]
    for row in shape:
        print(row)
    return

# @Profile(stats=PERFORMANCE_STATS)
def get_blank_shape(shape_lines):
    """
    Generate a blank shape. Used later to add extracted characters that make up
    one piece.
    """
    blank_shape_lines = [' ' * len(shape_line) for shape_line in shape_lines]
    return blank_shape_lines

# @Profile(stats=PERFORMANCE_STATS)
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
    shape_cells = {}
    shape_space_cells = set()
    shape_border_cells = set()
    for row, shape_line in enumerate(shape_lines):
        for col, cell_type in enumerate(shape_line):
            if cell_type == ' ':
                shape_space_cells.add((row, col, ' '))
            else:
                shape_border_cells = shape_border_cells.union({(row, col, dir_)
                                                               for dir_ in cell_types[cell_type]})
            shape_cells[(row, col)] = cell_types[cell_type]
    # TODO: check if shape_cell_q is still needed
    shape_cell_q = shape_space_cells.union(shape_border_cells)
    shape_inside = shape_cell_q.copy()
    # TODO: transform into Shape class
    return shape_cell_q, shape_cells, shape_inside, shape_space_cells, shape_border_cells

def get_white_piece_map(shape_neighbour_map, shape_inside, shape_white_spaces):
    shape_cell_to_white_piece_map = {}
    shape_white_pieces = {}
    white_piece_idx = 0
    main_q = shape_white_spaces.copy()
    piece_q = set()
    while main_q:
        piece_q.add(main_q.pop())
        white_piece = set()
        while piece_q:
            cell = piece_q.pop()
            white_piece.add(cell)
            row, col, _ = cell
            shape_cell_to_white_piece_map[(row, col)] = white_piece_idx
            # get neighbour cells
            neighbours = get_absolut_positions(cell, shape_neighbour_map[(row, col)])
            # remove neighbour cells that are outside the shape
            outside = neighbours.difference(shape_inside)
            if outside:
                # mark this white space as an outside element, this will not be a
                # valid piece
                shape_white_pieces[white_piece_idx] = '#'
                # remove all neighbour cells that are outside the shape
                neighbours = neighbours.difference(outside)
            # remove space cells already processed
            neighbours = neighbours.difference(white_piece)
            # remove all cells that are not white space cells
            neighbours = shape_white_spaces.intersection(neighbours)
            # add neighbours to work queue
            piece_q = piece_q.union(neighbours)
            # remove neighbours from main queue
            main_q = main_q.difference(neighbours)
        if white_piece_idx not in shape_white_pieces.keys():
            shape_white_pieces[white_piece_idx] = white_piece
        # TODO: rename to idx
        white_piece_idx += 1
    return shape_white_pieces, shape_cell_to_white_piece_map    

def get_pieces(shape_neighbour_map, shape_inside, shape_space_cells,
                   shape_border_cells, shape_white_pieces,
                   shape_cell_to_white_piece_map):
    # TODO: break into separate functions
    main_q = shape_border_cells.copy()
    idx = 0
    pieces = {}
    while main_q:
        single_piece_q = {main_q.pop()}
        piece = set()
        is_a_piece = True
        white_piece_added = False
        white_piece_idx = None
        while single_piece_q:
            cell = single_piece_q.pop()
            piece.add(cell)
            row, col, cell_type = cell
            # get all neighbour cells
            neighbours = VALID_NEIGHBOURS[cell_type].intersection(shape_neighbour_map[(row, col)])
            # transform relative positions to absolute positions
            neighbours = get_absolut_positions(cell, neighbours)
            # remove neighbour cells that are outside the shape
            outside = neighbours.difference(shape_inside)
            if outside:
                # mark this piece as an outside element, this will not be a
                # valid piece
                is_a_piece = False
                # remove all neighbour cells that are outside the shape
                neighbours = neighbours.difference(outside)
            # get all neighbour space cells 
            space_cells = shape_space_cells.intersection(neighbours)
            # when there is one or more space cell, get the index of the
            # white piece and store it in the border_to_white_piece_map
            if space_cells:
                # remove space cells from neighbours set (we only traverse along
                # piece cells)
                neighbours = neighbours.difference(space_cells)
                s_row, s_col, _ = space_cells.pop()
                white_piece_idx = shape_cell_to_white_piece_map[(s_row, s_col)]
                if shape_white_pieces[white_piece_idx] == '#':
                    is_a_piece = False
                elif not white_piece_added:
                    # add all white spaces to the piece
                    piece = piece.union(shape_white_pieces[white_piece_idx])
                    # we do this only once, all border cells point to the same
                    # white space piece
                    white_piece_added = True
            # remove neighbour cells that have been processed already (they are
            # no longer in the main_q)
            neighbours = neighbours.intersection(main_q)
            # remove neighbours from main work queue
            main_q = main_q.difference(neighbours)
            # add neighbours to work queue
            single_piece_q = single_piece_q.union(neighbours)
        if white_piece_idx != None and is_a_piece:
            p_idx = 'w{}'.format(white_piece_idx)
        elif is_a_piece:
            p_idx = 'b{}'.format(idx)
            idx += 1
        if is_a_piece and p_idx in pieces.keys():
            pieces[p_idx] = pieces[p_idx].union(piece)
        elif is_a_piece:
            pieces[p_idx] = piece
    return pieces

# @Profile(stats=PERFORMANCE_STATS)
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

# @Profile(stats=PERFORMANCE_STATS)
def get_absolut_positions(cell, neighbours):
    """
    Transform relative row, column coordinates into absolute coordinates.
    """
    row, col, _ = cell
    neighbours = {(row + d_row, col + d_col, cell_type)
                  for d_row, d_col, cell_type in neighbours}
    return neighbours

def set_to_dict(piece):
    dict_piece = {}
    for row, col, cell_type in piece:
        if (row, col) in dict_piece.keys():
            dict_piece[(row, col)].add(cell_type)
        else:
            dict_piece[(row, col)] = {cell_type}
    return dict_piece

# @Profile(stats=PERFORMANCE_STATS)
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

# @Profile(stats=PERFORMANCE_STATS)
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
+---+-+
|   | |
| +-+ |
| |   |
+-+---+

 +-+
 +-+

""".strip('\n')

#     INPUT_SHAPE = """
#             
#             
#   +-+-+  
#   | | |  
#   +-+-+  
#   |   |  
#   +---+  
#             
#             
# """.strip('\n')

#     INPUT_SHAPE = """
# ++
# ++
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

    ALL_PIECES = break_evil_pieces(INPUT_SHAPE)
    with open('break_the_pieces_evilized_edition.csv', 'w') as outfile:
        outfile.write('{}; {}; {}; {}\n'.format('function', 'time',
                                            'arguments', 'size of piece'))
        for entry in PERFORMANCE_STATS:
            text_line = ' '.join(['{};'.format(item) for item in entry]) + '\n'
            outfile.write(text_line)
    for counter, text_piece in enumerate(ALL_PIECES):
        print('\n{}.) piece:\n'.format(counter))
        print(text_piece)
    print()
