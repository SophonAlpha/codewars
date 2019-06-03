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
    row, col = get_starting_point(shape_lines)

    return

def get_starting_point(shape_lines):
    pattern = re.compile(r'\S')
    for row, shape_line in enumerate(shape_lines):
        match = pattern.search(shape_line)
        if match:
            col = match.start()
            break
    return row, col

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
    