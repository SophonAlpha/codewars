"""

Test suite 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

"""

import pytest

from solutions.break_the_pieces_evilized_edition import break_evil_pieces

TEST_CASES = [
{'name':'simple shape',
'shape': """
+----------+
|          |
|          |
|          |
+----------+
|          |
|          |
+----------+
""".strip('\n'),
        'expected': ["""
+----------+
|          |
|          |
|          |
+----------+
""".strip('\n'), """
+----------+
|          |
|          |
+----------+
""".strip('\n'),]},

{'name': '3 boxes',
'shape': """
+------------+
|            |
|            |
|            |
+------+-----+
|      |     |
|      |     |
+------+-----+
""".strip('\n'),
'expected': ["""
+------------+
|            |
|            |
|            |
+------------+
""".strip('\n'), """
+------+
|      |
|      |
+------+
""".strip('\n'), """
+-----+
|     |
|     |
+-----+
""".strip('\n'),]},

{'name': 'Lego stuff',
'shape': """
+-------------------+--+
|                   |  |
|                   |  |
|  +----------------+  |
|  |                   |
|  |                   |
+--+-------------------+
""".strip('\n'),
'expected': ["""
+-------------------+
|                   |
|                   |
|  +----------------+
|  |
|  |
+--+
""".strip('\n'), """
                 +--+
                 |  |
                 |  |
+----------------+  |
|                   |
|                   |
+-------------------+
""".strip('\n')]},

{'name': 'piece of cake! (check for irrelevant spaces)',
'shape': """
                           
                           
           +-+             
           | |             
         +-+-+-+           
         |     |           
      +--+-----+--+        
      |           |        
   +--+-----------+--+     
   |                 |     
   +-----------------+     
                           
                           
""".strip('\n'),
'expected': ["""
+-+
| |
+-+
""".strip('\n'), """
+-----+
|     |
+-----+
""".strip('\n'), """
+-----------+
|           |
+-----------+
""".strip('\n'), """
+-----------------+
|                 |
+-----------------+
""".strip('\n'),]},
        
{'name': 'horseshoe (shapes are not always rectangles!)',
'shape': """
+-----------------+
|                 |
|   +-------------+
|   |
|   |
|   |
|   +-------------+
|                 |
|                 |
+-----------------+
""".strip('\n'),
'expected': """
+-----------------+
|                 |
|   +-------------+
|   |
|   |
|   |
|   +-------------+
|                 |
|                 |
+-----------------+
""".strip('\n')},

{'name': 'warming up',
'shape': """
+------------+
|            |
|            |
|            |
+------++----+
|      ||    |
|      ||    |
+------++----+
""".strip('\n'),
'expected': ["""
+------------+
|            |
|            |
|            |
+------------+
""".strip('\n'), """
+------+
|      |
|      |
+------+
""".strip('\n'), """
+----+
|    |
|    |
+----+
""".strip('\n'), """
++
||
||
++
""".strip('\n')]},

{'name': 'don\'t forget the eggs! (you\'ll understand later...)',
'shape': """
++
++
""".strip('\n'),
'expected': """
++
++
""".strip('\n')}
]

@pytest.mark.parametrize('test_case', TEST_CASES)
def test_testcases(test_case):
    name = test_case['name']
    shape = test_case['shape']
    expected = test_case['expected']
    print(name)
    print(shape)
    pieces = break_evil_pieces(shape)
    for piece in pieces:
        print(piece)
        assert piece in expected
