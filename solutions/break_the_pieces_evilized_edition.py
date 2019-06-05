"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu
"""

import re

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
    piece = []
    piece = get_piece(row, col, shape_matrix, shape_lines, piece)
    print(row, col)
    return

def shape_to_matrix(shape_lines):
    matrix = {}
    for row, shape_line in enumerate(shape_lines):
        for col, cell in enumerate(shape_line):
            if cell == '+':
                matrix[(row, col)] = {'lr': True, 'll': True, 'ul': True, 'ur': True}
            if cell == '-':
                matrix[(row, col)] = {'u': True, 'd': True}
            if cell == '|':
                matrix[(row, col)] = {'r': True, 'l': True}
            if cell == ' ':
                matrix[(row, col)] = {'c': True}
    return matrix

def get_starting_point(shape_matrix):
    for entry in shape_matrix:
        if not 'c' in shape_matrix[entry].keys() and \
           sum(shape_matrix[entry].values()) < len(shape_matrix[entry].keys()):
            row, col = entry
            break
    return row, col

def get_piece(row, col, shape_matrix, shape_lines, piece, direction = 'free'):
    # TODO: remove piece from arguments list
    cell_type = get_cell_type(shape_lines, row, col)
    if not cell_type:
        return piece
    piece.append((row, col, cell_type))
    if direction == 'free':
        direction = get_next_direction(shape_matrix[row][col])
    if not direction:
        return piece
    cells_in_direction = {'lr': [( 0,  1): {'-': 'd', '+': 'll'},
                                 ( 1,  1): {' ': 'c', '+': 'ul'},
                                 ( 1,  0): {'|': 'r', '+': 'ur'}],
                          'll': [( 1,  0): {'|': 'l', '+': 'ul'},
                                 ( 1, -1): {' ': 'c', '+': 'ur'},
                                 ( 0, -1): {'-': 'd', '+': 'lr'}],
                          'ul': [( 0, -1),
                                 (-1, -1),
                                 (-1,  0)],
                          'ur': [(-1,  0), (-1,  1), ( 0,  1)],
                          'u' : [( 0, -1), (-1, -1), (-1,  0),
                                 (-1,  1), ( 0,  1)],
                          'd' : [( 0,  1), ( 1,  1), ( 1,  0),
                                 ( 1, -1), ( 0, -1)],
                          'r' : [(-1,  0), (-1,  1), ( 0,  1),
                                 ( 1,  1), ( 1,  0)],
                          'l' : [( 1,  0), ( 1, -1), ( 0, -1),
                                 (-1, -1), (-1,  0)],
                          'c' : [( 1,  0), ( 1,  1), ( 0,  1), (-1,  1),
                                 (-1,  0), (-1, -1), ( 0, -1), (-1, -1)]}
    for d_row, d_col in cells_in_direction[direction]:
        n_row = row + d_row
        n_col = col + d_col
        next_cell_type = get_cell_type(shape_lines, row + d_row, col + d_col)
        piece = get_piece(row, col + 1, shape_matrix, shape_lines, piece,
                          next_direction[(cell_type, direction, next_cell_type)])
                    
        shape_matrix[(row, col)]['c'] = False        
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
    