"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu
"""

import re

def break_evil_pieces(shape):
    shape_lines = shape.split('\n')
    pattern = re.compile(r'(?=([\+\|].*?[\+\|]))')
    for line in shape_lines:
        segments = pattern.match(line)
        for segment in segments:
            print(segment)
#         for segment in pattern.finditer(line):
#             print(segment.group(0), segment.start(), segment.end())
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
    