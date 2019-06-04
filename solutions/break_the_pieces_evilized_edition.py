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
                matrix[(row, col)] = {'lr': 0, 'll': 0, 'ul': 0, 'ur': 0}
            if cell == '-':
                matrix[(row, col)] = {'u': 0, 'd': 0}
            if cell == '|':
                matrix[(row, col)] = {'r': 0, 'l': 0}
            if cell == ' ':
                matrix[(row, col)] = {'c': 0}
    return matrix

def get_starting_point(shape_matrix):
    for entry in shape_matrix:
        if not 'c' in shape_matrix[entry].keys() and \
           sum(shape_matrix[entry].values()) < len(shape_matrix[entry].keys()):
            row, col = entry
            break
    return row, col

def get_piece(row, col, shape_matrix, shape_lines, piece, direction = None):
    # TODO: add test whether row, col is outside the shape boundary
    cell_type = shape_lines[row][col]
    piece.append((row, col, cell_type))
    if cell_type == '+':
        if shape_matrix[(row, col)]['lr'] == 0 and \
           direction in [None, 'd', 'r', 'ul', 'll', 'ur']:
            piece = get_piece(row, col + 1, shape_matrix,
                              shape_lines, piece, 'lr')
            piece = get_piece(row + 1, col, shape_matrix,
                              shape_lines, piece, 'lr')
            piece = get_piece(row + 1, col + 1, shape_matrix,
                              shape_lines, piece, 'lr')
            shape_matrix[(row, col)]['lr'] = 1
        if shape_matrix[(row, col)]['ll'] == 0 and \
           direction in [None, 'd', 'l', 'ur', 'lr', 'ul']:
            piece = get_piece(row, col - 1, shape_matrix,
                              shape_lines, piece, 'll')
            piece = get_piece(row + 1, col, shape_matrix,
                              shape_lines, piece, 'll')
            piece = get_piece(row + 1, col - 1, shape_matrix,
                              shape_lines, piece, 'll')
            shape_matrix[(row, col)]['ll'] = 1
        if shape_matrix[(row, col)]['ul'] == 0 and \
           direction in [None, 'u', 'l', 'lr', 'll', 'ur']:
            piece = get_piece(row, col - 1, shape_matrix,
                              shape_lines, piece, 'ul')
            piece = get_piece(row - 1, col, shape_matrix,
                              shape_lines, piece, 'ul')
            piece = get_piece(row - 1, col - 1, shape_matrix,
                              shape_lines, piece, 'ul')
            shape_matrix[(row, col)]['ul'] = 1
        if shape_matrix[(row, col)]['ur'] == 0 and \
           direction in [None, 'u', 'l', 'lr', 'll', 'ul']:
            piece = get_piece(row, col + 1, shape_matrix,
                              shape_lines, piece, 'ur')
            piece = get_piece(row - 1, col, shape_matrix,
                              shape_lines, piece, 'ur')
            piece = get_piece(row - 1, col + 1, shape_matrix,
                              shape_lines, piece, 'ur')
            shape_matrix[(row, col)]['ur'] = 1
    if cell_type == '-':
        if shape_matrix[(row, col)]['u'] == 0 and \
           direction in [None, 'u', 'ul', 'ur']:
            piece = get_piece(row, col + 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row - 1, col + 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row - 1, col, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row - 1, col - 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row, col - 1, shape_matrix,
                              shape_lines, piece, 'u')
            shape_matrix[(row, col)]['u'] = 1
        if shape_matrix[(row, col)]['d'] == 0 and \
           direction in [None, 'd', 'll', 'lr']:
            piece = get_piece(row, col + 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row + 1, col + 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row + 1, col, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row + 1, col - 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row, col - 1, shape_matrix,
                              shape_lines, piece, 'u')
            shape_matrix[(row, col)]['d'] = 1
    if cell_type == '|':
        if shape_matrix[(row, col)]['r'] == 0 and \
           direction in [None, 'r', 'ur', 'lr']:
            piece = get_piece(row, col + 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row - 1, col + 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row - 1, col, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row - 1, col - 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row, col - 1, shape_matrix,
                              shape_lines, piece, 'u')
            shape_matrix[(row, col)]['r'] = 1
        if shape_matrix[(row, col)]['l'] == 0 and \
           direction in [None, 'l', 'ul', 'll']:
            piece = get_piece(row, col + 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row + 1, col + 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row + 1, col, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row + 1, col - 1, shape_matrix,
                              shape_lines, piece, 'u')
            piece = get_piece(row, col - 1, shape_matrix,
                              shape_lines, piece, 'u')
            shape_matrix[(row, col)]['l'] = 1
    if cell_type == ' ':
        piece = get_piece(row, col + 1, shape_matrix,
                          shape_lines, piece, 'u')
        piece = get_piece(row + 1, col + 1, shape_matrix,
                          shape_lines, piece, 'u')
        piece = get_piece(row + 1, col, shape_matrix,
                          shape_lines, piece, 'u')
        piece = get_piece(row + 1, col - 1, shape_matrix,
                          shape_lines, piece, 'u')
        piece = get_piece(row, col - 1, shape_matrix,
                          shape_lines, piece, 'u')
        piece = get_piece(row - 1, col - 1, shape_matrix,
                          shape_lines, piece, 'u')
        piece = get_piece(row - 1, col, shape_matrix,
                          shape_lines, piece, 'u')
        piece = get_piece(row - 1, col + 1, shape_matrix,
                          shape_lines, piece, 'u')
        shape_matrix[(row, col)]['c'] = 1        
    return piece

def get_cells():

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
    ++
    ++
    
    +-----------------+
    |                 |
    |     +--+        |
    |     |  |        |
    |     +--+        |
    |                 |
    |            +----|
    |            |
    |      +-----+-----+
    |      |     |     |
    |      |     |     |
    +------+-----+-----+
           |     |     |
           |     |     |
           +-----+-----+
""".strip('\n')
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
    