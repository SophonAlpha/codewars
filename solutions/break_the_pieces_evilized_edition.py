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

NEXT_MAP = {
    'r': [('r', {(-1, 0, 'r')}), ('r', {(-1, 0, 'lr')}),],
    'l': [('l', {(1, 0, 'l')}), ('l', {(1, 0, 'ul')}),],
    'u': [('u', {(0, -1, 'u')}), ('u', {(0, -1, 'ur')}),],
    'd': [('d', {(0, 1, 'd')}), ('d', {(0, 1, 'll')}),],
    'lr': [('lr', {(0, 1, 'd'), (0, 1, 'll')}),
           ('ur', {(-1, 0, 'r'), (-1, 0, 'lr')}),
           ('ul', {(0, -1, 'u'), (0, -1, 'ur')}),
           ('ll', {(1, 0, 'l'), (1, 0, 'ul')}),],
    'ur': [('ur', {(-1, 0, 'r'), (-1, 0, 'lr')}),
           ('ul', {(0, -1, 'u'), (0, -1, 'ur')}),
           ('ll', {(1, 0, 'l'), (1, 0, 'ul')}),
           ('lr', {(0, 1, 'd'), (0, 1, 'll')}),],
    'ul': [('ul', {(0, -1, 'u'), (0, -1, 'ur')}),
           ('ll', {(1, 0, 'l'), (1, 0, 'ul')}),
           ('lr', {(0, 1, 'd'), (0, 1, 'll')}),
           ('ur', {(-1, 0, 'd'), (-1, 0, 'll')}),],
    'll': [('ll', {(1, 0, 'l'), (1, 0, 'ul')}),
           ('lr', {(0, 1, 'd'), (0, 1, 'll')}),
           ('ur', {(-1, 0, 'r'), (-1, 0, 'lr')}),
           ('ul', {(0, -1, 'u'), (0, -1, 'ur')}),],
    }

BESIDE = {
    'r': (0, 1), 'l': (0, -1), 'u': (-1, 0), 'd': (1, 0),
    'lr': (1, 1), 'ur': (-1, 1), 'ul': (-1, -1), 'll': (1, -1),
    }

class Shape:
    def __init__(self):
        self.txt_lines = []
        self.blank_lines = []
        self.cells = {}
        self.inside = set()
        self.space_cells = set()
        self.border_cells = set()
        self.neighbour_map = {}
        self.white_spaces = {}
        self.cell_to_white_space_map = {}
    
@Profile(stats=PERFORMANCE_STATS)
def break_evil_pieces(shape_txt):
    """
    main function

    Extract individual pieces from shape and return in list.
    """
    shape = Shape()
    shape.txt_lines = shape_txt.split('\n')
    shape = build_blank_shape(shape)
    shape = build_structures(shape)
    shape = build_neighbour_map(shape)
    shape = build_white_piece_map(shape)
    pieces = get_pieces(shape)
    txt_pieces = []
    for piece in pieces:
        piece = set_to_dict(piece)
        piece = plus_to_lines(piece)
        piece = piece_to_lines(piece, shape)
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

def DEBUG_display_piece(shape, piece):
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+',
                    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                    '6': '6', '7': '7', '8': '8', '9': '9',}
    txt_shape = shape.blank_lines[:]
    for row, col, cell_type in piece:
        txt_shape[row] = txt_shape[row][:col] + cell_to_char[cell_type] + txt_shape[row][col + 1:]
    for row in txt_shape:
        print(row)
    return

@Profile(stats=PERFORMANCE_STATS)
def build_blank_shape(shape):
    """
    Generate a blank shape. Used later to add extracted characters that make up
    one piece.
    """
    shape.blank_lines = [' ' * len(txt_line) for txt_line in shape.txt_lines]
    return shape

@Profile(stats=PERFORMANCE_STATS)
def build_structures(shape):
    """
    Transform the shape into several data structures that will be used for
    extracting individual pieces.

    shape.cells  - a dictionary that allows to address indiviual cells by
                   row, column
    shape.inside - all cells of the shape. This is used to detect whether a
                   row, column tuple is outside the shape (at the border).
                   It indicates that a set of cells is a border element and not
                   a valid piece.
    """
    cell_types = {'+': ['ul', 'ur', 'll', 'lr'],
                  '-': ['u', 'd'],
                  '|': ['r', 'l'],
                  ' ': [' '],}
    for row, shape_line in enumerate(shape.txt_lines):
        for col, cell_type in enumerate(shape_line):
            if cell_type == ' ':
                shape.space_cells.add((row, col, ' '))
            else:
                shape.border_cells = shape.border_cells.union({(row, col, dir_)
                                                               for dir_ in cell_types[cell_type]})
            shape.cells[(row, col)] = cell_types[cell_type]
    shape.inside = shape.space_cells.union(shape.border_cells)
    return shape

@Profile(stats=PERFORMANCE_STATS)
def build_white_piece_map(shape):
    idx = 0
    main_q = shape.space_cells.copy()
    piece_q = set()
    while main_q:
        piece_q.add(main_q.pop())
        white_piece = set()
        while piece_q:
            cell = piece_q.pop()
            white_piece.add(cell)
            row, col, _ = cell
            shape.cell_to_white_space_map[(row, col)] = idx
            # get neighbour cells
            neighbours = get_absolut_positions(cell, shape.neighbour_map[(row, col)])
            # remove neighbour cells that are outside the shape
            outside = neighbours.difference(shape.inside)
            if outside:
                # mark this white space as an outside element, this will not be a
                # valid piece
                shape.white_spaces[idx] = '#'
                # remove all neighbour cells that are outside the shape
                neighbours = neighbours.difference(outside)
            # remove space cells already processed
            neighbours = neighbours.difference(white_piece)
            # remove all cells that are not white space cells
            neighbours = shape.space_cells.intersection(neighbours)
            # add neighbours to work queue
            piece_q = piece_q.union(neighbours)
            # remove neighbours from main queue
            main_q = main_q.difference(neighbours)
        if idx not in shape.white_spaces.keys():
            shape.white_spaces[idx] = white_piece
        idx += 1
    return shape

@Profile(stats=PERFORMANCE_STATS)
def get_pieces(shape):
    main_q = shape.border_cells.copy()
    idx = 0
    borders = {}
    border_to_spaces_map = {}
    space_to_borders_map = {}
    while main_q:
        cell = main_q.pop()
        border = set()
        main_q, border, attached_white_spaces = get_one_border(main_q, cell, shape)
        if border:
            borders[idx] = border
            if attached_white_spaces:
                space_to_borders_map = add_to_white_space_map(attached_white_spaces,
                                                              idx,
                                                              space_to_borders_map)
                border_to_spaces_map = add_to_border_map(attached_white_spaces,
                                                         idx,
                                                         border_to_spaces_map)
            idx += 1
    segments = join_segments(space_to_borders_map, border_to_spaces_map)
    pieces = join_pieces(borders, segments)
    return pieces

@Profile(stats=PERFORMANCE_STATS)
def add_to_white_space_map(attached_white_spaces, border_idx, space_to_borders_map):
    for white_space in attached_white_spaces:
        if white_space in space_to_borders_map.keys():
            space_to_borders_map[white_space].add(border_idx)                    
        else:
            space_to_borders_map[white_space] = {border_idx}
    return space_to_borders_map    

@Profile(stats=PERFORMANCE_STATS)
def add_to_border_map(attached_white_spaces, border_idx, border_to_spaces_map):
    if border_idx in border_to_spaces_map.keys():
        border_to_spaces_map[border_idx].add(attached_white_spaces)
    else:
        border_to_spaces_map[border_idx] = attached_white_spaces
    return border_to_spaces_map

@Profile(stats=PERFORMANCE_STATS)
def join_segments(space_to_borders_map, border_to_spaces_map):
    segments = []
    border_IDs = list(border_to_spaces_map.keys())
    while border_IDs:
        border = border_IDs[0]
        segment = set()
        work_q = set()
        work_q.add(border)
        while work_q:
            border = work_q.pop()
            border_IDs.remove(border)
            segment.add(border)
            for space in border_to_spaces_map[border]:
                work_q = work_q.union(space_to_borders_map[space])
            work_q = work_q.difference(segment)
        segments.append(segment)
    return segments

@Profile(stats=PERFORMANCE_STATS)
def join_pieces(borders, segments):
    border_IDs = list(borders.keys())
    pieces = []
    for segment in segments:
        piece = set()
        for border_ID in segment:
            piece = piece.union(borders[border_ID])
            border_IDs.remove(border_ID)
        pieces.append(piece)
    for border_ID in border_IDs:
        pieces.append(borders[border_ID])
    return pieces

@Profile(stats=PERFORMANCE_STATS)
def get_one_border(main_q, cell, shape):
    is_a_border = True
    border = set()
    attached_white_spaces = set()
    while cell not in border:
        row, col, cell_type = cell
        # check if cell is at the outside of shape
        d_row, d_col = BESIDE[cell_type]
        b_pos = (row + d_row, col + d_col)
        if b_pos not in shape.cells.keys():
            is_a_border = False
        # check if beside the cell there is white space
        if b_pos in shape.cell_to_white_space_map.keys():
            key = shape.cell_to_white_space_map[b_pos]
            attached_white_spaces.add(key)
            if shape.white_spaces[key] == '#':
                is_a_border = False
        cell, border, main_q = get_next_cell(cell, border, main_q, shape)
    if not is_a_border:
        border = False
    return main_q, border, attached_white_spaces

@Profile(stats=PERFORMANCE_STATS)
def get_next_cell(cell, border, main_q, shape):
    # get neighbours of current cell
    row, col, cell_type = cell
    neighbours = shape.neighbour_map[(row, col)]
    for n_type, valid_neighbours in NEXT_MAP[cell_type]:
        # add cell to border
        border.add((row, col, n_type))
        # remove processed cell from main queue
        main_q = main_q.difference({(row, col, n_type)})
        # check for valid neighbour cells combination
        neighbour_cells = neighbours.intersection(valid_neighbours)
        if len(neighbour_cells) > 0:
            n_row, n_col, n_cell_type = neighbour_cells.pop()
            cell = (row + n_row, col + n_col, n_cell_type)
            break
    return cell, border, main_q

@Profile(stats=PERFORMANCE_STATS)
def build_neighbour_map(shape):
    """
    Build a dictionary data structure where for each cell (a row, column tuple)
    all neighbouring cells are returned.
    """
    deltas = [(-1, 0), (-1, 1), (0, 1), (1, 1),
              (1, 0), (1, -1), (0, -1), (-1, -1),]
    for row, col in shape.cells:
        neighbour_cells = set()
        for d_row, d_col in deltas:
            n_row, n_col = row + d_row, col + d_col
            if (n_row, n_col) in shape.cells.keys():
                new_set = {(d_row, d_col, cell)
                           for cell in shape.cells[(n_row, n_col)]}
                neighbour_cells = neighbour_cells.union(new_set)
            else:
                neighbour_cells.add((d_row, d_col, '#'))
        shape.neighbour_map[(row, col)] = neighbour_cells
    return shape

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
def set_to_dict(piece):
    dict_piece = {}
    for row, col, cell_type in piece:
        if (row, col) in dict_piece.keys():
            dict_piece[(row, col)].add(cell_type)
        else:
            dict_piece[(row, col)] = {cell_type}
    return dict_piece

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
    if (row - 1, col) in piece.keys() and \
        piece[row - 1, col].intersection({'l', 'r', 'll', 'lr'}) and \
        (row + 1, col) in piece.keys() and \
        piece[row + 1, col].intersection({'l', 'r', 'ul', 'ur'}) and \
        ((row, col - 1) not in piece.keys() or \
        ((row, col - 1) in piece.keys() and \
         piece[row, col - 1].intersection({'l', 'r'}))) and \
        ((row, col + 1) not in piece.keys() or \
        ((row, col + 1) in piece.keys() and \
         piece[row, col + 1].intersection({'l', 'r'}))):
        piece[row, col] = {'l', 'r'}
    elif (row, col - 1) in piece.keys() and \
        piece[row, col - 1].intersection({'u', 'd', 'ur', 'lr'}) and \
        (row, col + 1) in piece.keys() and \
        piece[row, col + 1].intersection({'u', 'd', 'ul', 'll'}) and \
        ((row - 1, col) not in piece.keys() or \
        ((row - 1, col) in piece.keys() and \
         piece[row - 1, col].intersection({'u', 'd'}))) and \
        ((row + 1, col) not in piece.keys() or \
        ((row + 1, col) in piece.keys() and \
         piece[row + 1, col].intersection({'u', 'd'}))):
        piece[row, col] = {'u', 'd'}
    return piece

@Profile(stats=PERFORMANCE_STATS)
def piece_to_lines(piece, shape):
    """
    Transform the piece matrix into a list of text lines.
    """
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+'}
    shape_txt = shape.blank_lines[:]
    for row, col in piece.keys():
        cell = piece[(row, col)].pop()
        shape_txt[row] = shape_txt[row][:col] + cell_to_char[cell] + shape_txt[row][col + 1:]
    return shape_txt

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
        outfile.write('{}; {}\n'.format('function', 'time'))
        for entry in PERFORMANCE_STATS:
            text_line = ' '.join(['{};'.format(item) for item in entry]) + '\n'
            outfile.write(text_line)
    for counter, text_piece in enumerate(ALL_PIECES):
        print('\n{}.) piece:\n'.format(counter))
        print(text_piece)
    print()
