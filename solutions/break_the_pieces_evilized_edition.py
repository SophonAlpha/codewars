"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu
"""

import re

def break_evil_pieces(shape):
    shape_lines = shape.split('\n')
    pattern = re.compile(r'(?=(?P<line>[\+\|]-*?[\+\|]))'
                         r'|(?=(?P<segment>[\+\|] *?[\+\|]))')
    for line in shape_lines:
        for segment in pattern.finditer(line):            
            print(segment.lastgroup, segment.group(segment.lastgroup),
                  segment.start(segment.lastgroup),
                  segment.end(segment.lastgroup))
    return

if __name__ == '__main__':
    shape = """
+------------+
|            |
|            |
|            |
|      +-----+-----+
|      |     |     |
|      |     |     |
+------+-----+-----+
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
    