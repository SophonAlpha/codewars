"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu
"""

import re

TRANSITIONS = {
    'lr': {( 0,  1): {'-': 'd', '+': 'll', ' ': 'c'},
           ( 1,  1): {' ': 'c', '+': 'ul', ' ': 'c'},
           ( 1,  0): {'|': 'r', '+': 'ur', ' ': 'c'}},
    'll': {( 1,  0): {'|': 'l', '+': 'ul', ' ': 'c'},
           ( 1, -1): {' ': 'c', '+': 'ur', ' ': 'c'},
           ( 0, -1): {'-': 'd', '+': 'lr', ' ': 'c'}},
    'ul': {( 0, -1): {'-': 'u', '+': 'ur', ' ': 'c'},
           (-1, -1): {' ': 'c', '+': 'lr', ' ': 'c'},
           (-1,  0): {'|': 'l', '+': 'll', ' ': 'c'}},
    'ur': {(-1,  0): {'|': 'r', '+': 'lr', ' ': 'c'},
           (-1,  1): {' ': 'c', '+': 'll', ' ': 'c'},
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
           (-1,  1): {' ': 'c', '+': 'll', '|': 'r', '-': 'd'},
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

class Segment:
    
    def __init__(self, match):
        self.type = match.lastgroup
        self.string = match.group(self.type)
        self.start = match.start(self.type)
        self.end = match.end(self.type)

def break_evil_pieces(shape):
    shape_lines = shape.split('\n')
    blank_shape_lines = get_blank_shape(shape_lines)
    shape_matrix = shape_to_matrix(shape_lines)
    row, col = get_starting_point(shape_matrix)
    piece = get_piece(row, col, shape_matrix, shape_lines)
    piece = piece_to_shape(piece, blank_shape_lines)
    print(piece)
    return

def get_blank_shape(shape_lines):
    blank_shape_lines = [' ' * len(shape_line) for shape_line in shape_lines]
    return blank_shape_lines

def shape_to_matrix(shape_lines):
    matrix = mark_outer_area(shape_lines)
    for row, shape_line in enumerate(shape_lines):
        for col, cell in enumerate(shape_line):
            if cell == '+':
                matrix[(row, col)] = {
                    'ul': is_outer_area(row - 1, col, matrix),
                    'ur': is_outer_area(row - 1, col, matrix),
                    'll': is_outer_area(row + 1, col, matrix),
                    'lr': is_outer_area(row + 1, col, matrix)}
            if cell == '-':
                matrix[(row, col)] = {
                    'u': is_outer_area(row - 1, col, matrix),
                    'd': is_outer_area(row + 1, col, matrix)}
            if cell == '|':
                matrix[(row, col)] = {
                    'r': is_outer_area(row, col + 1, matrix),
                    'l': is_outer_area(row, col - 1, matrix)}
            if cell == ' ':
                if not (row, col) in matrix.keys():
                    matrix[(row, col)] = {'c': True}
    return matrix

def is_outer_area(row, col, matrix):
    if not (row, col) in matrix.keys():
        return False
    if 'c' in matrix[row, col].keys():
        status = matrix[row, col]['c']
    return status

def mark_outer_area(shape_lines):
    outer_area = []
    pattern = re.compile(r'(^ *).*?( *)$')
    for shape_line in shape_lines:
        match = pattern.fullmatch(shape_line)
        if match:
            line = shape_line
            for idx in range(1, match.lastindex + 1):
                start = match.start(idx)
                end = match.end(idx)
                line = line[:start] + 'o' * (end - start) + line[end:]
            outer_area.append(line)
    return outer_area

def get_starting_point(shape_matrix):
    for entry in shape_matrix:
        if not 'c' in shape_matrix[entry].keys() and \
           sum(shape_matrix[entry].values()) > 0:
            row, col = entry
            break
    return row, col

def get_piece(row, col, shape_matrix, shape_lines):
    queue = []
    direction = get_next_direction(shape_matrix[(row, col)])
    queue.append((row, col, direction))
    piece = []
    while queue:
        row, col, direction = queue.pop()
        cell_type = get_cell_type(shape_lines, row, col)
        piece.append((row, col, cell_type))
        shape_matrix[(row, col)][direction] = False
        for d_row, d_col in TRANSITIONS[direction]:
            n_row = row + d_row
            n_col = col + d_col
            next_cell_type = get_cell_type(shape_lines, n_row, n_col)
            next_direction = TRANSITIONS[direction][d_row, d_col][next_cell_type]
            if next_cell_type and \
               shape_matrix[(n_row, n_col)][next_direction] and \
               not (n_row, n_col, next_direction) in queue:
                queue.append((n_row, n_col, next_direction))
    return piece

def piece_to_shape(piece, blank_shape_lines):
    shape = blank_shape_lines
    for row, col, cell_type in piece:
        shape[row] = shape[row][:col] + cell_type + shape[row][col + 1:]
    shape = remove_outer_area(shape)
    return shape

def remove_outer_area(shape):
    shape_new = []    
    for row in shape:
        line = row.strip()
        if line:
            shape_new.append(line)
    return shape_new

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

def break_evil_pieces_v1(shape):
    shape_lines = shape.split('\n')
    pattern = re.compile(r'(?=(?P<line>[\+\|]-*?[\+\|]))'
                         r'|(?=(?P<segment>[\+\|] *?[\+\|]))')
    pieces = []
    for line_idx, shape_line in enumerate(shape_lines):
        for match in pattern.finditer(shape_line):
            segment = Segment(match)
            pieces = segment_to_piece(segment, line_idx, pieces)
    return

def segment_to_piece(segment, line_idx, pieces):
    for pos, piece in enumerate(pieces):
        if piece[-1]['start'] <= segment.start <= piece[-1]['end'] and \
           piece[-1]['start'] <= segment.end <= piece[-1]['end']:
            pieces[pos].append({'line': line_idx,
                                'start': segment.start,
                                'end': segment.end,
                                'string': segment.string})
    if segment.type == 'line':
        pieces = add_piece(segment, line_idx, pieces)
    return pieces

def add_piece(segment, line_idx, pieces):
    pieces.append([{'line': line_idx,
                    'start': segment.start,
                    'end': segment.end,
                    'string': segment.string}])
    return pieces
    
if __name__ == '__main__':
    shape = """
        
  +--+  
  |  |  
  +--+  
        
""".strip('\n')

# """
#     ++
#     ++
#     
#     +-----------------+
#     |                 |
#     |     +--+        |
#     |     |  |        |
#     |     +--+        |
#     |                 |
#     |            +----|
#     |            |
#     |      +-----+-----+
#     |      |     |     |
#     |      |     |     |
#     +------+-----+-----+
#            |     |     |
#            |     |     |
#            +-----+-----+
# """.strip('\n')
    expected = ["""
+------------+
|            |
|            |
|            |
|      +-----+
|      |      
|      |      
+------+      
""".strip('\n'), """
+-----+
|     |
|     |
+-----+
""".strip('\n'), """
+-----+
|     |
|     |
+-----+
""".strip('\n')]
    pieces = break_evil_pieces(shape)
    