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

    2019-07-22:
        approach "white pieces + border tracing + join together",
        runtime: 0.38s

    2019-07-28:
        approach "white pieces & border tracing combined",
        runtime: 0.40s

    2019-07-31:
        approach "trace space neighbours & border tracing combined",
        runtime: 0.095s

    2019-08-10:
        approach "reduced redundancy in space cells tests & border
        tracing combined",
        runtime: 0.058s

    2019-08-12:
        approach "removed more redundancy in space cells tests & border
        tracing combined",
        runtime: 0.038s
"""

import re
from solutions.performance import Profile

PERFORMANCE_STATS = []

DELTA = [
    (-1, 0), (0, 1), (1, 0), (0, -1)
]
VALID_NEIGHBOURS = {
    (-1, 0): {'ll', 'lr', 'd', ' '},
    (-1, 1): {'ll', 'l', 'd', ' '},
    (0, 1): {'ll', 'ul', 'l', ' '},
    (1, 1): {'ul', 'l', 'u', ' '},
    (1, 0): {'ul', 'ur', 'u', ' '},
    (1, -1): {'ur', 'u', 'r', ' '},
    (0, -1): {'ur', 'lr', 'r', ' '},
    (-1, -1): {'lr', 'r', 'd', ' '},
}
NEXT_STEP = {
    'u': ((0, -1), {'u', 'ur'}), 'd': ((0, 1), {'d', 'll'}),
    'r': ((-1, 0), {'r', 'lr'}), 'l': ((1, 0), {'l', 'ul'}),
    'ur': ((-1, 0), {'r', 'lr'}), 'lr': ((0, 1), {'d', 'll'}),
    'll': ((1, 0), {'l', 'ul'}), 'ul': ((0, -1), {'u', 'ur'}),
}
PLUS_SEQUENCE = {
    'ur': 'ul', 'ul': 'll', 'll': 'lr', 'lr': 'ur',
}
OPPOSITES = {
    'r': {'l', 'ul', 'll'}, 'l': {'r', 'ur', 'lr'}, 'u': {'d', 'lr', 'll'},
    'd': {'u', 'ul', 'ur'}, 'ur': {'ll', 'l', 'd'}, 'lr': {'ul', 'l', 'u'},
    'll': {'ur', 'r', 'u'}, 'ul': {'lr', 'r', 'd'}
}
BESIDE = {
    'r': (0, 1), 'l': (0, -1), 'u': (-1, 0), 'd': (1, 0),
    'lr': (1, 1), 'ur': (-1, 1), 'ul': (-1, -1), 'll': (1, -1),
}


class Shape:
    """
    Data structure to hold various pre-calculated information to accelerate
    the piece search.
    """

    def __init__(self):
        self.txt_lines = []
        self.blank_lines = []
        self.cells = set()
        self.cell_pos = {}
        self.inside = set()
        self.space_cells = set()
        self.border_cells = set()
        self.space_neighbour_map = {}
        self.no_neighbours = {}


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
    txt_pieces = []
    for piece in get_pieces(shape):
        piece = set_to_dict(piece)
        piece = plus_to_lines(piece)
        piece = piece_to_text_lines(piece, shape)
        piece = trim_piece(piece)
        txt_pieces.append(piece)
    return txt_pieces


def debug_display_white_piece_map(shape_white_pieces, shape_cells, blank_shape_lines):
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+',
                    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                    '6': '6', '7': '7', '8': '8', '9': '9', }
    shape = blank_shape_lines[:]
    for idx in shape_white_pieces:
        for row, col, _ in shape_white_pieces[idx]:
            shape_cells[(row, col)] = ['{}'.format(idx % 9)]
    for row, col in shape_cells.keys():
        cell = shape_cells[(row, col)][0]
        shape[row] = shape[row][:col] + cell_to_char[cell] + shape[row][col + 1:]
    for row in shape:
        print(row)


def debug_display_piece(shape, piece):
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+',
                    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                    '6': '6', '7': '7', '8': '8', '9': '9', }
    txt_shape = shape.blank_lines[:]
    for row, col, cell_type in piece:
        txt_shape[row] = txt_shape[row][:col] + \
                         cell_to_char[cell_type] + \
                         txt_shape[row][col + 1:]
    for row in txt_shape:
        print(row)


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
    Build a number of data structures that accelerate the search for border
    and space elements.
    """
    type_map = {'+': {'ul', 'ur', 'll', 'lr'},
                '-': {'u', 'd'},
                '|': {'r', 'l'},
                ' ': {' '}, }
    for row, shape_line in enumerate(shape.txt_lines):
        for col, type_char in enumerate(shape_line):
            if type_char == ' ':
                shape.space_cells.add(((row, col, type_char)))
            else:
                for cell_type in type_map[type_char]:
                    shape.border_cells.add((row, col, cell_type))
            shape.cell_pos[(row, col)] = type_map[type_char]
            shape.inside.add((row, col))
    shape.cells = shape.border_cells.union(shape.space_cells)
    return shape


@Profile(stats=PERFORMANCE_STATS)
def get_pieces(shape):
    """
    Generator that returns one piece after the other.
    """
    cell_q = shape.cells.copy()
    while cell_q:
        cell = cell_q.pop()
        piece = set()
        is_a_piece = True
        piece_q = set()
        piece_q.add(cell)
        while piece_q:
            cell = piece_q.pop()
            _, _, cell_type = cell
            if cell_type == ' ':
                is_outside, \
                border_cells, \
                space_cells = process_space_cells(cell, shape)
                piece_q = piece_q.difference(space_cells)
                border_cells = border_cells.difference(piece)
                piece_q = piece_q.union(border_cells)
            else:
                is_outside, \
                border_cells, \
                space_cells = process_border_cells(cell, shape)
                piece = piece.union(border_cells)
                piece_q = piece_q.difference(border_cells)
                space_cells = space_cells.intersection(cell_q)
                piece_q = piece_q.union(space_cells)
            if is_outside:
                is_a_piece = False
            cell_q = cell_q.difference(space_cells)
            cell_q = cell_q.difference(border_cells)
        if is_a_piece:
            yield piece


@Profile(stats=PERFORMANCE_STATS)
def process_space_cells(cell, shape):
    """
    Find all space cells starting from one cell.
    """
    is_outside = False
    border_cells = set()
    space_cells = set()
    processed_cells = set()
    piece_q = set()
    row, col, _ = cell
    piece_q.add((row, col))
    while piece_q:
        row, col = piece_q.pop()
        space_cells.add((row, col, ' '))
        processed_cells.add((row, col))
        for d_row, d_col in DELTA:
            n_row, n_col = row + d_row, col + d_col
            if ((n_row, n_col) not in processed_cells and
                    (n_row, n_col) not in piece_q):
                # test if we are outside the shape
                if (n_row, n_col) not in shape.inside:
                    # mark this piece as an outside element, this will not be a
                    # valid piece
                    is_outside = True
                elif (' ' in shape.cell_pos[(n_row, n_col)] and
                      (n_row, n_col, ' ') not in space_cells):
                    piece_q.add((n_row, n_col))
                else:
                    neighbours = VALID_NEIGHBOURS[(d_row, d_col)]
                    cell_types = shape.cell_pos[(n_row, n_col)]
                    cell_types = cell_types.intersection(neighbours)
                    for cell_type in cell_types:
                        border_cells.add((n_row, n_col, cell_type))
                        processed_cells.add((n_row, n_col))
    return is_outside, border_cells, space_cells


@Profile(stats=PERFORMANCE_STATS)
def process_border_cells(cell, shape):
    """
    Find all border cells starting from one cell.
    """
    is_outside = False
    border_cells = set()
    space_cells = set()
    piece_q = set()
    piece_q.add(cell)
    next_cell = cell
    while piece_q:
        cell = piece_q.pop()
        if cell not in border_cells:
            row, col, cell_type = cell
            # add cell to piece
            border_cells.add(cell)
            # test if space cell is next to the cell
            d_row, d_col = BESIDE[cell_type]
            t_row, t_col = row + d_row, col + d_col
            test_cell = (t_row, t_col, ' ')
            if test_cell in shape.space_cells:
                space_cells.add(test_cell)
            # test if there is a border element next to the cell
            if (t_row, t_col) in shape.inside:
                next_cell_type = shape.cell_pos[(t_row, t_col)]
                next_cell_type = next_cell_type.intersection(OPPOSITES[cell_type])
                if next_cell_type:
                    next_cell = (t_row, t_col, next_cell_type.pop())
                    if next_cell not in border_cells:
                        piece_q.add(next_cell)
            # test if this border faces towards the outside the shape
            if (cell_type in ['r', 'l', 'u', 'd'] and
                    not (t_row, t_col) in shape.inside):
                # mark this border as an outside element, not a valid piece
                is_outside = True
            # get the next cell along the border
            (d_row, d_col), possible_types = NEXT_STEP[cell_type]
            n_row, n_col = row + d_row, col + d_col
            next_cell_type = None
            if (n_row, n_col) in shape.inside:
                next_cell_type = shape.cell_pos[(n_row, n_col)]
                next_cell_type = next_cell_type.intersection(possible_types)
            else:
                # mark this border as an outside element, not a valid piece
                is_outside = True
            if next_cell_type:
                next_cell_type = next_cell_type.pop()
                next_cell = (n_row, n_col, next_cell_type)
            else:
                # get next corner cell
                next_cell_type = PLUS_SEQUENCE[cell_type]
                next_cell = (row, col, next_cell_type)
            piece_q.add(next_cell)
    return is_outside, border_cells, space_cells


@Profile(stats=PERFORMANCE_STATS)
def set_to_dict(piece):
    """
    Transform a set into a dictionary with the row, column pair as the key.
    """
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
            ((row - 1, col) not in piece.keys() or \
             piece[row - 1, col].intersection({'u', 'd'})):
        piece[row, col] = {'u'}
    elif piece[row, col] == {'ll', 'lr'} and \
            ((row + 1, col) not in piece.keys() or \
             piece[row + 1, col].intersection({'u', 'd'})):
        piece[row, col] = {'d'}
    elif piece[row, col] == {'ul', 'll'} and \
            ((row, col - 1) not in piece.keys() or \
             piece[row, col - 1].intersection({'r', 'l'})):
        piece[row, col] = {'l'}
    elif piece[row, col] == {'ur', 'lr'} and \
            ((row, col + 1) not in piece.keys() or \
             piece[row, col + 1].intersection({'r', 'l'})):
        piece[row, col] = {'r'}
    return piece


@Profile(stats=PERFORMANCE_STATS)
def piece_to_text_lines(piece, shape):
    """
    Transform the piece matrix into a list of text lines.
    """
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+'}
    shape_txt = shape.blank_lines[:]
    for row, col in piece.keys():
        cell = piece[(row, col)].pop()
        shape_txt[row] = (shape_txt[row][:col] +
                          cell_to_char[cell] +
                          shape_txt[row][col + 1:])
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
            min_start = (start if min_start is None or
                                  min_start > start else min_start)
    shape_new = []
    for row in shape:
        if row.strip():
            shape_new.append(row[min_start:].rstrip())
    shape_new = '\n'.join(shape_new)
    return shape_new


if __name__ == '__main__':
    #     INPUT_SHAPE = """
    # +----+
    # |    |
    # |    |
    # |    |
    # |    |
    # +----+
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
