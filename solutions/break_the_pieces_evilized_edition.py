"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu
"""

import re

NEXT_DIRECTIONS = {
    'lr': {( 0,  1): {'-': 'd', '+': 'll'},
           ( 1,  1): {' ': 'c', '+': 'ul'},
           ( 1,  0): {'|': 'r', '+': 'ur'}},
    'll': {( 1,  0): {'|': 'l', '+': 'ul'},
           ( 1, -1): {' ': 'c', '+': 'ur'},
           ( 0, -1): {'-': 'd', '+': 'lr'}},
    'ul': {( 0, -1): {'-': 'u', '+': 'ur'},
           (-1, -1): {' ': 'c', '+': 'lr'},
           (-1,  0): {'|': 'l', '+': 'll'}},
    'ur': {(-1,  0): {'|': 'r', '+': 'lr'},
           (-1,  1): {' ': 'c', '+': 'll'},
           ( 0,  1): {'-': 'u', '+': 'ul'}},
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
    shape_matrix = shape_to_matrix(shape_lines)
    row, col = get_starting_point(shape_matrix)
    piece = get_piece(row, col, shape_matrix, shape_lines)
    piece = piece_to_shape(piece)
    print(piece)
    return

def shape_to_matrix(shape_lines):
    matrix = {}
    for row, shape_line in enumerate(shape_lines):
        matrix = mark_outer_area(shape_line, matrix, row)
        for col, cell in enumerate(shape_line):
            if cell == '+':
                matrix[(row, col)] = {'lr': True, 'll': True, 'ul': True, 'ur': True}
            if cell == '-':
                matrix[(row, col)] = {'u': True, 'd': True}
            if cell == '|':
                matrix[(row, col)] = {'r': True, 'l': True}
            if cell == ' ':
                if not (row, col) in matrix.keys():
                    matrix[(row, col)] = {'c': True}
    return matrix

def mark_outer_area(shape_line, matrix, row):
    pattern = re.compile(r'(^ *).*?( *)$')
    match = pattern.fullmatch(shape_line)
    if match:
        for idx in range(1, match.lastindex + 1):
            start = match.start(idx)
            end = match.end(idx)
            for col in range(start, end):
                matrix[(row, col)] = {'c': False}
    return matrix

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
        for d_row, d_col in NEXT_DIRECTIONS[direction]:
            n_row = row + d_row
            n_col = col + d_col
            next_cell_type = get_cell_type(shape_lines, n_row, n_col)
            next_direction = NEXT_DIRECTIONS[direction][d_row, d_col][next_cell_type]
            if next_cell_type and \
               shape_matrix[(n_row, n_col)][next_direction] and \
               not (n_row, n_col, next_direction) in queue:
                queue.append((n_row, n_col, next_direction))
    return piece

def piece_to_shape(piece):
    shape = []
    for row, col, cell_type in piece:
        try:
            shape[row]
        except IndexError:
            shape
        pass

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
    