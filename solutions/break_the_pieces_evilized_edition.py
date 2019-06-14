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
TRANSITIONS = {
    'lr': {( 0,  1): {'-': 'd', '+': 'll', ' ': 'c'},
           ( 1,  1): {'|': 'l', '+': 'ul', ' ': 'c'},
           ( 1,  0): {'|': 'r', '+': 'ur', ' ': 'c'}},
    'll': {( 1,  0): {'|': 'l', '+': 'ul', ' ': 'c'},
           ( 1, -1): {'|': 'r', '+': 'ur', ' ': 'c'},
           ( 0, -1): {'-': 'd', '+': 'lr', ' ': 'c'}},
    'ul': {( 0, -1): {'-': 'u', '+': 'ur', ' ': 'c'},
           (-1, -1): {'|': 'r', '+': 'lr', ' ': 'c'},
           (-1,  0): {'|': 'l', '+': 'll', ' ': 'c'}},
    'ur': {(-1,  0): {'|': 'r', '+': 'lr', ' ': 'c'},
           (-1,  1): {'|': 'l', '+': 'll', ' ': 'c'},
           ( 0,  1): {'-': 'u', '+': 'ul', ' ': 'c'}},
    'u' : {( 0, -1): {'-': 'u', '+': 'ur'},
           (-1, -1): {' ': 'c', '+': 'lr', '|': 'r', '-': 'd'},
           (-1,  0): {' ': 'c', '-': 'd'},
           (-1,  1): {' ': 'c', '+': 'll', '|': 'l', '-': 'd'},
           ( 0,  1): {'-': 'u', '+': 'ul'}},
    'd' : {( 0,  1): {'-': 'd', '+': 'll'},
           ( 1,  1): {' ': 'c', '+': 'ul', '|': 'l', '-': 'u'},
           ( 1,  0): {' ': 'c', '-': 'u'},
           ( 1, -1): {' ': 'c', '+': 'ur', '|': 'r', '-': 'u'},
           ( 0, -1): {'-': 'd', '+': 'lr'}},
    'r' : {(-1,  0): {'|': 'r', '+': 'lr'},
           (-1,  1): {' ': 'c', '+': 'll', '|': 'l', '-': 'd'},
           ( 0,  1): {' ': 'c', '|': 'l'},
           ( 1,  1): {' ': 'c', '+': 'ul', '|': 'l', '-': 'u'},
           ( 1,  0): {'|': 'r', '+': 'ur'}},
    'l' : {( 1,  0): {'|': 'l', '+': 'ul'},
           ( 1, -1): {' ': 'c', '+': 'ur', '|': 'r', '-': 'u'},
           ( 0, -1): {' ': 'c', '|': 'r'},
           (-1, -1): {' ': 'c', '+': 'lr', '|': 'r', '-': 'd'},
           (-1,  0): {'|': 'l', '+': 'll'}},
    'c' : {( 0,  1): {' ': 'c', '+': 'll', '|': 'l'},
           ( 1,  1): {' ': 'c', '+': 'ul', '|': 'l', '-': 'u'},
           ( 1,  0): {' ': 'c', '+': 'ur', '-': 'u'},
           ( 1, -1): {' ': 'c', '+': 'ur', '|': 'r', '-': 'u'},
           ( 0, -1): {' ': 'c', '+': 'ur', '|': 'r'},
           (-1, -1): {' ': 'c', '+': 'lr', '|': 'r', '-': 'd'},
           (-1,  0): {' ': 'c', '+': 'll', '-': 'd'}, 
           (-1,  1): {' ': 'c', '+': 'll', '|': 'l', '-': 'd'}}}

def break_evil_pieces(shape):
    """
    main function

    Extract individual pieces from shape and return in list.
    """
    pieces = []
    shape_lines = shape.split('\n')
    blank_shape_lines = get_blank_shape(shape_lines)
    shape_matrix = shape_to_matrix(shape_lines)
    row, col = get_starting_point(shape_matrix)
    while not row is None and not col is None:
        piece = get_piece(row, col, shape_matrix, shape_lines)
        piece = plus_to_lines(piece)
        piece = piece_to_lines(piece, blank_shape_lines)
        piece = trim_piece(piece)
        pieces.append(piece)
        row, col = get_starting_point(shape_matrix)
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
    cells = []
    matrix = empty_matrix(shape_lines)
    for row, shape_line in enumerate(shape_lines):
        for col, cell in enumerate(shape_line):
            if cell == '+':
                matrix[row][col] = {'ul': True, 'ur': True,
                                    'll': True, 'lr': True}
                cells.append((row, col, cell))
            elif cell == '-':
                matrix[row][col] = {'u': True, 'd': True}
                cells.append((row, col, cell))
            elif cell == '|':
                matrix[row][col] = {'r': True, 'l': True}
                cells.append((row, col, cell))
            elif cell == ' ':
                matrix[row][col] = {'c': True}
        matrix = mark_outer_line(matrix, row, shape_line)
    matrix = mark_outer_area(matrix, cells)
    return matrix

def empty_matrix(shape_lines):
    """
    Generate an empty matrix.
    """
    matrix = []
    for _, shape_line in enumerate(shape_lines):
        matrix.append([{}] * len(shape_line))
    return matrix

def mark_outer_line(matrix, row, shape_line):
    """
    Mark the ' ' cells that are 'outer' part of a line. Outer part is not
    enclosed by '+', '-', and '|' characters and therefore cannot belong
    to any piece.
    """
    pattern = re.compile(r'(^ *).*?( *)$')
    match = pattern.fullmatch(shape_line)
    if match:
        for idx in range(1, match.lastindex + 1):
            start = match.start(idx)
            end = match.end(idx)
            for col in range(start, end):
                matrix[row][col] = {'c': False}
    return matrix

def mark_outer_area(matrix, cells):
    """
    For the '+', '-', and '|' cells mark the section that belongs to the outer
    part.
    """
    for row, col, cell in cells:
        if cell == '+':
            matrix[row][col]['ul'] = is_outer_area(row - 1, col, matrix) and \
                                     is_outer_area(row, col - 1, matrix) and \
                                     is_outer_area(row - 1, col - 1, matrix)
            matrix[row][col]['ur'] = is_outer_area(row - 1, col, matrix) and \
                                     is_outer_area(row, col + 1, matrix) and \
                                     is_outer_area(row - 1, col + 1, matrix)
            matrix[row][col]['ll'] = is_outer_area(row + 1, col, matrix) and \
                                     is_outer_area(row, col - 1, matrix) and \
                                     is_outer_area(row + 1, col - 1, matrix)
            matrix[row][col]['lr'] = is_outer_area(row + 1, col, matrix) and \
                                     is_outer_area(row, col + 1, matrix) and \
                                     is_outer_area(row + 1, col + 1, matrix)
        elif cell == '-':
            matrix[row][col]['u'] = is_outer_area(row - 1, col, matrix)
            matrix[row][col]['d'] = is_outer_area(row + 1, col, matrix)
        elif cell == '|':
            matrix[row][col]['r'] = is_outer_area(row, col + 1, matrix)
            matrix[row][col]['l'] = is_outer_area(row, col - 1, matrix)
    return matrix

def is_outer_area(row, col, matrix):
    """
    Detect if cells is outer part.
    """
    if 0 <= row <= len(matrix) - 1 and 0 <= col <= len(matrix[row]) - 1:
        if 'c' in matrix[row][col].keys():
            status = matrix[row][col]['c']
        else:
            status = True
    else:
        status = False
    return status

def get_starting_point(shape_matrix):
    """
    Return a staring point for detecting a piece. If no starting point can be
    found return None, None (usually this means all pieces have been found).
    """
    s_row, s_col = None, None
    for row, _ in enumerate(shape_matrix):
        for col, _ in enumerate(shape_matrix[row]):
            if not 'c' in shape_matrix[row][col].keys() and \
               sum(shape_matrix[row][col].values()) > 0:
                s_row = row
                s_col = col
                return s_row, s_col
    return s_row, s_col

def get_piece(row, col, shape_matrix, shape_lines):
    """
    Extract one piece. Uses a flood filling algorithm.
    """
    queue = []
    direction = get_next_direction(shape_matrix[row][col])
    queue.append((row, col, direction))
    piece = []
    while queue:
        row, col, direction = queue.pop()
        cell_type = get_cell_type(shape_lines, row, col)
        piece.append((row, col, cell_type))
        shape_matrix[row][col][direction] = False
        for d_row, d_col in TRANSITIONS[direction]:
            n_row = row + d_row
            n_col = col + d_col
            next_cell_type = get_cell_type(shape_lines, n_row, n_col)
            next_direction = TRANSITIONS[direction][d_row, d_col][next_cell_type]
            if next_cell_type and \
               shape_matrix[n_row][n_col][next_direction] and \
               (n_row, n_col, next_direction) not in queue:
                queue.append((n_row, n_col, next_direction))
    return piece

def get_cell_type(shape_lines, row, col):
    """
    Get the cell type.
    """
    try:
        cell_type = shape_lines[row][col]
    except IndexError:
        return False
    return cell_type

def get_next_direction(directions):
    """
    For cells with multiple possible directions select the next possible one.
    """
    direction = None
    for val in iter(directions):
        if directions[val]:
            direction = val
            break
    return direction

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
+------------+
|            |
|            |
+------++----+
|      ||    |
|      ||    |
+------++----+
""".strip('\n')
    break_evil_pieces(INPUT_SHAPE)
    