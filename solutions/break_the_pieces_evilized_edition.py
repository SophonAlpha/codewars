"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu
"""

import re

def break_evil_pieces(shape):
    """
    main function

    Extract individual pieces from shape and return in list.
    """
    pieces = []
    shape_lines = shape.split('\n')
    blank_shape_lines = get_blank_shape(shape_lines)
    shape_matrix = shape_to_matrix(shape_lines)
    shape_matrix = remove_loose_ends(shape_matrix)
    cells_to_be_processed = list(shape_matrix.keys())
    while cells_to_be_processed:
        cell = cells_to_be_processed[0]
        piece = get_piece(cell, cells_to_be_processed, shape_matrix)
        if piece:
            piece = piece_to_lines(piece, blank_shape_lines)
            piece = trim_piece(piece)
            pieces.append(piece)
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
    Transform the text lines into a data structure for processing.
    Each cell is transformed into 2 x 2 cells. For each cell a set of
    characters indicates which border line is set. The characters have the
    following meaning: 'r' - right, 'l' - left, 'b' - bottom, 't' - top.

    An example: a single cell with the character '+' at row 0 and
    column 0 = (0, 0) is translated into the following four cells:
        (0, 0,) = {'r', 'b'}, (0, 1) = {'l', 'b'},
        (1, 0) = {'r', 't'}, (1, 1) = {'l', 't'}
    """
    shape_matrix = {}
    mapping = {
        ' ': [[0, 0, set()], [0, 1, set()], [1, 0, set()], [1, 1, set()]],
        '+': [[0, 0, {'r', 'b'}], [0, 1, {'l', 'b'}],
              [1, 0, {'r', 't'}], [1, 1, {'l', 't'}]],
        '-': [[0, 0, {'b'}], [0, 1, {'b'}], [1, 0, {'t'}], [1, 1, {'t'}]],
        '|': [[0, 0, {'r'}], [0, 1, {'l'}], [1, 0, {'r'}], [1, 1, {'l'}]]
        }
    for row, shape_line in enumerate(shape_lines):
        for col, cell_type in enumerate(shape_line):
            for d_row, d_col, borders in mapping[cell_type]:
                shape_matrix[(row * 2 + d_row, col * 2 + d_col)] = borders
    return shape_matrix

def remove_loose_ends(shape_matrix):
    """
    For all '+' characters the lines that are not connected need to be removed.
    This is a neccessary preparation for later to correctly test whether
    a piece is closed and not just the outside area around a piece.
    """
    deltas = [{'r': (-1, 0), 'b': (0, -1)},
              {'l': (-1, 0), 'b': (0, 1)},
              {'r': (1, 0), 't': (0, -1)},
              {'l': (1, 0), 't': (0, 1)}]
    for cell in shape_matrix.keys():
        neighbours = [entry for entry in deltas
                      if set(entry.keys()) == shape_matrix[cell]]
        if neighbours:
            borders = neighbours[0]
            for border in borders:
                cell_to_check = tuple(map(sum, zip(cell, borders[border])))
                if not cell_to_check in shape_matrix or \
                   not shape_matrix[cell_to_check].intersection(set(border)):
                    shape_matrix[cell] = shape_matrix[cell].difference(border)
    return shape_matrix

def get_piece(cell, cells_to_be_processed, shape_matrix):
    """
    Extract a single piece given a start cell.
    """
    deltas = {'t': (-1, 0), 'b': (1, 0), 'l': (0, -1), 'r': (0, 1)}
    piece, edges, work_q = {}, [], []
    start_cell = cell
    work_q.append(start_cell)
    while work_q:
        cell = work_q.pop()
        row, col = cell
        piece[(row, col)] = shape_matrix[(row, col)]
        del cells_to_be_processed[cells_to_be_processed.index(cell)]
        for direction in {'t', 'b', 'r', 'l'}.difference(shape_matrix[cell]):
            d_row, d_col = deltas[direction]
            next_row, next_col = row + d_row, col + d_col
            if (next_row, next_col) in cells_to_be_processed and \
               (next_row, next_col) not in work_q:
                work_q.append((next_row, next_col))
        edges = add_edge(cell, piece[cell], start_cell, edges)
    if not is_inside_piece(start_cell, edges):
        return None
    return piece

def add_edge(cell, cell_type, start_cell, edges):
    """
    Build a list of all vertical edges at the same row as the start cell. This
    will later be used to detect whether a test point is inside or outside a
    piece.
    """
    deltas = {'r': (0, 1, 1, 1), 'l': (0, 0, 1, 0)}
    start_row, _ = start_cell
    row, _ = cell
    cell_type = cell_type.intersection({'r', 'l'})
    if row == start_row and cell_type:
        cell_type = list(cell_type)[0]
        edge = tuple(map(sum, zip(cell + cell, deltas[cell_type])))
        if edge not in edges:
            edges.append(edge)
    return edges

def is_inside_piece(start_cell, edges):
    """
    Test wether a piece is closed and not just the area outside the piece. This
    is done using the ray casting algorithm (crossing number algorithm or
    even-odd rule algorithm). A test point is placed at what we expect to be
    inside the piece. We cast a horizontal ray from the test point and count
    how many times it crosses the boundary. If it is odd, the point is
    inside, even the point is outside.
    """
    result = False
    cross_points_right, cross_points_left = 0, 0
    start_x, start_y = start_cell
    test_x, test_y = start_x + 0.25, start_y + 0.25
    for edge_start_x, edge_start_y, edge_end_x, edge_end_y in edges:
        if  edge_start_x <= test_x < edge_end_x or \
            edge_end_x <= test_x < edge_start_x:
            v_1 = (edge_start_x, edge_start_y,
                   edge_end_x - edge_start_x, edge_end_y - edge_start_y)
            v_2 = (test_x, test_y, 0, 1)
            _, t_2 = vector_intersection(v_1, v_2)
            if t_2 < 0:
                cross_points_right += 1
            else:
                cross_points_left += 1
    if cross_points_right % 2 != 0 and cross_points_left % 2 != 0:
        result = True
    return result

def vector_intersection(v_1, v_2):
    """
    Calculate the intersection between two lines using Cramer's rule.
    """
    p1x, p1y, d1x, d1y = v_1
    p2x, p2y, d2x, d2y = v_2
    c_x, c_y = p2x - p1x, p2y - p1y
    m_div = d1y * d2x - d1x * d2y
    t_1 = (c_y * d2x - c_x * d2y) / m_div if m_div != 0 else None
    t_2 = (d1x * c_y - d1y * c_x) / m_div if m_div != 0 else None
    return t_1, t_2

def piece_to_lines(piece, blank_shape_lines):
    """
    Transform the piece matrix into a list of text lines.
    """
    deltas = [(0, 0), (0, 1), (1, 0), (1, 1)]
    shape = blank_shape_lines[:]
    work_q = list(piece.keys())
    while work_q:
        row, col = work_q.pop()
        row, col = (row // 2) * 2, (col // 2) * 2
        cells = [(row + d_row, col + d_col) for d_row, d_col in deltas]
        for cell in cells:
            if cell in work_q:
                del work_q[work_q.index(cell)]
        cell_types = [elem for elem in [piece[cell] for cell in cells
                                        if cell in piece.keys()]]
        cell_types = set().union(*cell_types)
        if not cell_types:
            cell_char = ' '
        elif cell_types.intersection({'r', 'l'}) and \
             cell_types.intersection({'t', 'b'}):
            cell_char = '+'
        elif cell_types.intersection({'r', 'l'}):
            cell_char = '|'
        elif cell_types.intersection({'t', 'b'}):
            cell_char = '-'
        s_row, s_col = row // 2, col // 2
        shape[s_row] = shape[s_row][:s_col] + cell_char + shape[s_row][s_col + 1:]
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
++++
+--+
""".strip('\n')
    for text_piece in break_evil_pieces(INPUT_SHAPE):
        print('-----------------------')
        print(text_piece)
