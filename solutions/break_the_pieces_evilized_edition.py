"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu
"""

import re

# The TRANSITION dictionary is used for the flood fill algorithm. For any cell the
# algorithm can only 'flood' in specific directions. The TRANSITION dictionary
# provides for a given direction the relative coordinates of the next cells to be
# filled. In addition, for each relative coordinate it also provides the valid
# next directions.
#
# The dictionary keys have the following meanings:
#
#     ul - upper left corner
#     ur - upper right corner
#     ll - lower left corner
#     lr - lower right corner
#     u  - upper half
#     l  - lower half
#     r  - right half
#     l  - left half
#     c  - center
TRANSITION = {
    'ur': [['ur', ['r', 'lr']],
           ['ul', ['u', 'ur']],
           ['ll', ['l', 'ul']],
           ['lr', ['d', 'll']]],
    'ul': [['ul', ['u', 'ur']],
           ['ll', ['l', 'ul']],
           ['lr', ['d', 'll']],
           ['ur', ['r', 'lr']]],
    'll': [['ll', ['l', 'ul']],
           ['lr', ['d', 'll']],
           ['ur', ['r', 'lr']],
           ['ul', ['u', 'ur']]],
    'lr': [['lr', ['d', 'll']],
           ['ur', ['r', 'lr']],
           ['ul', ['u', 'ur']],
           ['ll', ['l', 'ul']]],
    'u': [['u', ['u', 'ur']]],
    'd': [['d', ['d', 'll']]],
    'l': [['l', ['l', 'ul']]],
    'r': [['r', ['r', 'lr']]],
    }
NEIGHBOUR = {'r': (-1, 0), 'l': (1, 0), 'd': (0, 1), 'u': (0, -1),
             'lr': (0, 1), 'll': (1, 0), 'ul': (0, -1), 'ur': (-1, 0)}
OFFSET = {'r': (0, 0.25), 'l': (0, -0.25),
          'd': (0.25, 0), 'u': (-0.25, 0),
          'lr': (0.25, 0.25), 'll': (0.25, -0.25),
          'ul': (-0.25, -0.25), 'ur': (-0.25, 0.25)}

def break_evil_pieces(shape):
    """
    main function

    Extract individual pieces from shape and return in list.
    """
    pieces = []
    shape_lines = shape.split('\n')
    blank_shape_lines = get_blank_shape(shape_lines)
    shape_matrix = shape_to_matrix(shape_lines)
    cell = get_start_cell(shape_matrix)
    while cell:
        piece = get_piece(cell, shape_matrix, shape_lines)
        if piece:
            piece = plus_to_lines(piece)
            piece = piece_to_lines(piece, blank_shape_lines)
            piece = trim_piece(piece)
            pieces.append(piece)
        cell = get_start_cell(shape_matrix)
    return pieces

def get_blank_shape(shape_lines):
    """
    Generate a blank shape. Used later to add extracted characters that make up
    one piece.
    """
    blank_shape_lines = [' ' * len(shape_line) for shape_line in shape_lines]
    return blank_shape_lines

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
    For ' ' cells: c - center
    """
    matrix = {}
    for row, shape_line in enumerate(shape_lines):
        for col, cell in enumerate(shape_line):
            if cell == '+':
                matrix[(row, col, 'ul')] = True
                matrix[(row, col, 'ur')] = True
                matrix[(row, col, 'll')] = True
                matrix[(row, col, 'lr')] = True
            elif cell == '-':
                matrix[(row, col, 'u')] = True
                matrix[(row, col, 'd')] = True
            elif cell == '|':
                matrix[(row, col, 'r')] = True
                matrix[(row, col, 'l')] = True
    return matrix

def get_start_cell(shape_matrix):
    """
    Return a staring point for detecting a piece. If no starting point can be
    found return None, None (usually this means all pieces have been found).
    """
    for row, col, direction in shape_matrix.keys():
        if shape_matrix[(row, col, direction)]:
            return row, col, direction
    return False

def get_piece(cell, shape_matrix, shape_lines):
    """
    Extract one piece. Uses a track the border algorithm.
    """
    start_cell = cell
    piece = []
    edges = []
    while cell and not is_piece_complete(piece, cell, shape_lines):
        if cell_already_visited(cell, shape_matrix):
            piece = None
            return piece
        row, col, _ = cell
        piece.append((row, col, shape_lines[row][col]))
        next_cell = get_next_cell(cell, shape_matrix)
        shape_matrix[cell] = False
        edges = add_edge(cell, next_cell, start_cell, edges)
        cell = next_cell
    if not (cell and is_inside_piece(start_cell, edges)):
        piece = None
    return piece

def cell_already_visited(cell, shape_matrix):
    return not shape_matrix[cell]

def get_next_cell(cell, shape_matrix):
    row, col, start_direction = cell
    for neighbour_directions in TRANSITION[start_direction]:
        direction = neighbour_directions[0]
        for next_direction in neighbour_directions[1]:
            d_row, d_col = NEIGHBOUR[direction]
            next_row, next_col = row + d_row, col + d_col
            next_cell = (next_row, next_col, next_direction)
            if next_cell in shape_matrix.keys():
                return next_cell
    return None

def add_edge(cell, next_cell, start_cell, edges):
    start_row, _, _ = start_cell
    row, col, _ = cell
    next_row, next_col, _ = next_cell
    if (row == start_row or next_row == start_row) and \
        row != next_row:
        edges.append((row, col, next_row, next_col))
    return edges

def is_piece_complete(piece, cell, shape_lines):
    row, col, _ = cell
    return (row, col, shape_lines[row][col]) in piece

def is_inside_piece(start_cell, edges):
    result = False
    cross_points_right, cross_points_left = 0, 0
    start_x, start_y, direction = start_cell
    offset_x, offset_y = OFFSET[direction]
    test_x, test_y = start_x + offset_x, start_y + offset_y
    for edge_start_x, edge_start_y, edge_end_x, edge_end_y in edges:
        if  edge_start_x <= test_x < edge_end_x or \
            edge_end_x <= test_x < edge_start_x:
            v1 = (edge_start_x, edge_start_y,
                  edge_end_x - edge_start_x, edge_end_y - edge_start_y)
            v2 = (test_x, test_y, 0, 1)
            _, t2 = vector_intersection(v1, v2)
            if t2 < 0:
                cross_points_right += 1
            else:
                cross_points_left += 1
    if cross_points_right % 2 != 0 and cross_points_left % 2 != 0:
        result = True
    return result

def vector_intersection(v1, v2):
    """
    Calculate the intersection between two lines using Cramer's rule.
    """
    p1x, p1y, d1x, d1y = v1
    p2x, p2y, d2x, d2y = v2
    cx, cy = p2x - p1x, p2y - p1y
    m = d1y * d2x - d1x * d2y
    t1 = (cy * d2x - cx * d2y) / m if m != 0 else None
    t2 = (d1x * cy - d1y * cx) / m if m != 0 else None
    return t1, t2

def plus_to_lines(piece):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    for row, col, cell_type in piece:
        if cell_type == '+':
            piece = should_be_line(row, col, piece)
    return piece

def should_be_line(row, col, piece):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    index = piece.index((row, col, '+'))
    horizontal = [(row, col + delta) for delta in [1, -1]]
    result = all([(row, col, '-') in piece or \
                  (row, col, '+') in piece for row, col in horizontal])
    if result:
        piece[index] = (row, col, '-')
        return piece
    vertical = [(row + delta, col) for delta in [1, -1]]
    result = all([(row, col, '|') in piece or \
                  (row, col, '+') in piece for row, col in vertical])
    if result:
        piece[index] = (row, col, '|')
        return piece
    return piece

def piece_to_lines(piece, blank_shape_lines):
    """
    Transform the piece matrix into a list of text lines.
    """
    shape = blank_shape_lines[:]
    for row, col, cell_type in piece:
        shape[row] = shape[row][:col] + cell_type + shape[row][col + 1:]
    return shape

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
      
 +-+ 
 | | 
 +-+ 
 | | 
 +-+ 
      
""".strip('\n')
    for text_piece in break_evil_pieces(INPUT_SHAPE):
        print('-----------------------')
        print(text_piece)
