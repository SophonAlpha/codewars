"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu
"""

import re

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
    pieces = []
    shape_lines = shape.split('\n')
    blank_shape_lines = get_blank_shape(shape_lines)
    shape_matrix = shape_to_matrix(shape_lines)
    row, col = get_starting_point(shape_matrix)
    while not row == None and not col == None:
        piece = get_piece(row, col, shape_matrix, shape_lines)
        piece = plus_to_lines(piece)
        piece = piece_to_lines(piece, blank_shape_lines)
        piece = trim_piece(piece)
        pieces.append(piece)
        row, col = get_starting_point(shape_matrix)
    return pieces

def get_blank_shape(shape_lines):
    blank_shape_lines = [' ' * len(shape_line) for shape_line in shape_lines]
    return blank_shape_lines

def shape_to_matrix(shape_lines):
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
    matrix = []
    for _, shape_line in enumerate(shape_lines):
        matrix.append([{}] * len(shape_line))
    return matrix 

def mark_outer_line(matrix, row, shape_line):
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
    if 0 <= row <= len(matrix) - 1 and 0 <= col <= len(matrix[row]) - 1:
        if 'c' in matrix[row][col].keys():
            status = matrix[row][col]['c']
        else:
            status = True
    else:
        status = False
    return status

def get_starting_point(shape_matrix):
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
               not (n_row, n_col, next_direction) in queue:
                queue.append((n_row, n_col, next_direction))
    return piece

def get_cell_type(shape_lines, row, col):
    try:
        cell_type = shape_lines[row][col]
    except IndexError:
        return False
    return cell_type

def get_next_direction(directions):
    direction = None
    for val in iter(directions):
        if directions[val]:
            direction = val
            break
    return direction

def plus_to_lines(piece):
    for row, col, cell_type in piece:
        if cell_type == '+':
            piece = should_be_line(row, col, piece)
    return piece

def should_be_line(row, col, piece):
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
    shape = blank_shape_lines[:]
    for row, col, cell_type in piece:
        shape[row] = shape[row][:col] + cell_type + shape[row][col + 1:]
    return shape

def trim_piece(shape):
    min_start = None
    pattern = re.compile(r'(^ *)(?P<shape>.*?)( *)$')
    for row in shape:
        match = pattern.fullmatch(row)
        if match.group('shape'):
            start = match.start('shape')
            min_start = start if min_start == None or min_start > start else min_start
    shape_new = []
    for row in shape:
        if row.strip():
            shape_new.append(row[min_start:].rstrip())
    shape_new = '\n'.join(shape_new)
    return shape_new
    
if __name__ == '__main__':
    shape = """
+------------+
|            |
|            |
+------++----+
|      ||    |
|      ||    |
+------++----+
""".strip('\n')
    pieces = break_evil_pieces(shape)
    