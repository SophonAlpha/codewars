"""
My solution for 'Break the pieces (Evilized Edition)' kata:
https://www.codewars.com/kata/break-the-pieces-evilized-edition

Level: 1 kyu

Performance optimizations:

    reference shape size: 67 rows, 59 columns

    2019-06-29
        approach "2x2 sub-cells",
        runtime: 10.93s

        approach "2x2 sub-cells, process white spaces",
        runtime: 11.33s

    2019-07-12
        approach "original shape (no sub-cells), traverse via dictionary",
        runtime: 8.44s

    2019-07-14
        approach "build neighbours for each cell and set intersection",
        runtime: 2.33s

    2019-07-15
        approach "replace loops with set operations in get_neighbours()",
        runtime: 0.57s
        
    2019-07-22:
        approach "white pieces + border tracing + join together",
        runtime: 0.38s
"""

import re
from solutions.performance import Profile

PERFORMANCE_STATS = []

NEXT_MAP = {
    'r': [('r', {(-1, 0, 'r')}), ('r', {(-1, 0, 'lr')}),],
    'l': [('l', {(1, 0, 'l')}), ('l', {(1, 0, 'ul')}),],
    'u': [('u', {(0, -1, 'u')}), ('u', {(0, -1, 'ur')}),],
    'd': [('d', {(0, 1, 'd')}), ('d', {(0, 1, 'll')}),],
    'lr': [('lr', {(0, 1, 'd'), (0, 1, 'll')}),
           ('ur', {(-1, 0, 'r'), (-1, 0, 'lr')}),
           ('ul', {(0, -1, 'u'), (0, -1, 'ur')}),
           ('ll', {(1, 0, 'l'), (1, 0, 'ul')}),],
    'ur': [('ur', {(-1, 0, 'r'), (-1, 0, 'lr')}),
           ('ul', {(0, -1, 'u'), (0, -1, 'ur')}),
           ('ll', {(1, 0, 'l'), (1, 0, 'ul')}),
           ('lr', {(0, 1, 'd'), (0, 1, 'll')}),],
    'ul': [('ul', {(0, -1, 'u'), (0, -1, 'ur')}),
           ('ll', {(1, 0, 'l'), (1, 0, 'ul')}),
           ('lr', {(0, 1, 'd'), (0, 1, 'll')}),
           ('ur', {(-1, 0, 'd'), (-1, 0, 'll')}),],
    'll': [('ll', {(1, 0, 'l'), (1, 0, 'ul')}),
           ('lr', {(0, 1, 'd'), (0, 1, 'll')}),
           ('ur', {(-1, 0, 'r'), (-1, 0, 'lr')}),
           ('ul', {(0, -1, 'u'), (0, -1, 'ur')}),],
    }

BESIDE = {
    'r': (0, 1), 'l': (0, -1), 'u': (-1, 0), 'd': (1, 0),
    'lr': (1, 1), 'ur': (-1, 1), 'ul': (-1, -1), 'll': (1, -1),
    }

class Shape:
    def __init__(self):
        # TODO: check if all these variables are required
        self.txt_lines = []
        self.blank_lines = []
        self.cells = set()
        self.cell_pos = {}
        self.inside = set()
        self.space_cells = set()
        self.border_cells = set()

# class Shape_v1:
#     def __init__(self):
#         self.txt_lines = []
#         self.blank_lines = []
#         self.cells = {}
#         self.inside = set()
#         self.space_cells = set()
#         self.border_cells = set()
#         self.neighbour_map = {}
#         self.white_spaces = {}
#         self.borders = {}
#         self.cell_space_map = {}
#         self.cell_border_map = {}
#         self.border_to_borders_map = {}
#         self.space_to_borders_map = {}
#         self.border_to_spaces_map = {}

@Profile(stats=PERFORMANCE_STATS)
def break_evil_pieces(shape_txt):
    """
    main function

    Extract individual pieces from shape and return in list.
    """
    shape = Shape()
    shape.txt_lines = shape_txt.split('\n')
    shape = build_blank_shape(shape)
    shape = build_structures(shape)
    txt_pieces = []
    # TODO: check if spaces can be removed from pieces
    for piece in get_pieces(shape):
        piece = set_to_dict(piece)
        piece = plus_to_lines(piece, shape)
        piece = piece_to_text_lines(piece, shape)
        piece = trim_piece(piece)
        txt_pieces.append(piece)
    return txt_pieces

def DEBUG_display_white_piece_map(shape_white_pieces, shape_cells, blank_shape_lines):
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+',
                    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                    '6': '6', '7': '7', '8': '8', '9': '9',}
    shape = blank_shape_lines[:]
    for idx in shape_white_pieces:
        for row, col, _ in shape_white_pieces[idx]:
            shape_cells[(row, col)] = ['{}'.format(idx % 9)]
    for row, col in shape_cells.keys():
        cell = shape_cells[(row, col)][0]
        shape[row] = shape[row][:col] + cell_to_char[cell] + shape[row][col + 1:]
    for row in shape:
        print(row)
    return

def DEBUG_display_piece(shape, piece):
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+',
                    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                    '6': '6', '7': '7', '8': '8', '9': '9',}
    txt_shape = shape.blank_lines[:]
    for row, col, cell_type in piece:
        txt_shape[row] = txt_shape[row][:col] + cell_to_char[cell_type] + txt_shape[row][col + 1:]
    for row in txt_shape:
        print(row)
    return

@Profile(stats=PERFORMANCE_STATS)
def build_blank_shape(shape):
    """
    Generate a blank shape. Used later to add extracted characters that make up
    one piece.
    """
    shape.blank_lines = [' ' * len(txt_line) for txt_line in shape.txt_lines]
    return shape

# @Profile(stats=PERFORMANCE_STATS)
def build_structures(shape):
    type_map = {'+': {'ul', 'ur', 'll', 'lr'},
                '-': {'u', 'd'},
                '|': {'r', 'l'},
                ' ': {' '},}
    for row, shape_line in enumerate(shape.txt_lines):
        for col, type_char in enumerate(shape_line):
            if type_char == ' ':
                shape.space_cells.add(((row, col, type_char)))
            else:
                for cell_type in type_map[type_char]:
                    shape.border_cells.add((row, col, cell_type))
            shape.cell_pos[(row, col)] = type_map[type_char]
            shape.inside.add((row, col))
    shape.cells = shape.border_cells.union(shape.space_cells)
    return shape

# @Profile(stats=PERFORMANCE_STATS)
def build_structures_v1(shape):
    """
    Transform the shape into several data structures that will be used for
    extracting individual pieces.
    """
    cell_types = {'+': ['ul', 'ur', 'll', 'lr'],
                  '-': ['u', 'd'],
                  '|': ['r', 'l'],
                  ' ': [' '],}
    for row, shape_line in enumerate(shape.txt_lines):
        for col, cell_type in enumerate(shape_line):
            if cell_type == ' ':
                shape.space_cells.add((row, col, ' '))
            else:
                shape.border_cells = shape.border_cells.union({(row, col, dir_)
                                                               for dir_ in cell_types[cell_type]})
            shape.cells[(row, col)] = set(cell_types[cell_type])
    shape.inside = shape.space_cells.union(shape.border_cells)
    return shape

@Profile(stats=PERFORMANCE_STATS)
def build_white_piece_map(shape):
    idx = 0
    main_q = shape.space_cells.copy()
    piece_q = set()
    while main_q:
        piece_q.add(main_q.pop())
        white_piece = set()
        while piece_q:
            cell = piece_q.pop()
            white_piece.add(cell)
            row, col, _ = cell
            shape.cell_space_map[(row, col)] = idx
            # get neighbour cells
            neighbours = get_absolut_positions(cell, shape.neighbour_map[(row, col)])
            # remove neighbour cells that are outside the shape
            outside = neighbours.difference(shape.inside)
            if outside:
                # mark this white space as an outside element, this will not be a
                # valid piece
                shape.white_spaces[idx] = '#'
                # remove all neighbour cells that are outside the shape
                neighbours = neighbours.difference(outside)
            # remove space cells already processed
            neighbours = neighbours.difference(white_piece)
            # remove all cells that are not white space cells
            neighbours = shape.space_cells.intersection(neighbours)
            # add neighbours to work queue
            piece_q = piece_q.union(neighbours)
            # remove neighbours from main queue
            main_q = main_q.difference(neighbours)
        if idx not in shape.white_spaces.keys():
            shape.white_spaces[idx] = white_piece
        idx += 1
    return shape

def get_pieces(shape):
    """
    Get all the pieces.    
    """
    cell_q = shape.cells.copy()
    while cell_q:
        cell = cell_q.pop()
        piece = set()
        is_a_piece = True
        piece_q = set()
        piece_q.add(cell)
        while piece_q:
            cell = piece_q.pop()
            _, _, cell_type = cell
            if cell_type == ' ':
                is_outside, border_cells, space_cells = process_space_cells(cell, shape)
                piece = piece.union(space_cells)
                piece_q = piece_q.difference(space_cells)
                border_cells = border_cells.difference(piece)
                piece_q = piece_q.union(border_cells)
            else:
                is_outside, border_cells, space_cells = process_border_cells(cell, shape)
                piece = piece.union(border_cells)
                piece_q = piece_q.difference(border_cells)
                space_cells = space_cells.difference(piece)
                piece_q = piece_q.union(space_cells)
            if is_outside:
                is_a_piece = False
            cell_q = cell_q.difference(space_cells)
            cell_q = cell_q.difference(border_cells)
        if is_a_piece:
            yield piece
    return

def process_space_cells(cell, shape):
    # TODO: move this up as a constant
    deltas = {(-1, 0, ' '), (-1, 0, 'd'), (-1, 1, ' '), (-1, 1, 'll'),
              (0, 1, ' '), (0, 1, 'l'), (1, 1, ' '), (1, 1, 'ul'),
              (1, 0, ' '), (1, 0, 'u'), (1, -1, ' '), (1, -1, 'ur'),
              (0, -1, ' '), (0, -1, 'r'), (-1, -1, ' '), (-1, -1, 'lr'),}
    is_outside = False
    border_cells = set()
    space_cells = set()
    piece_q = set()
    piece_q.add(cell)
    while piece_q:
        cell = piece_q.pop()
        space_cells.add(cell)
        # get neighbour cells
        neighbours = deltas
        neighbours = get_absolut_positions(cell, neighbours)
        # test if there are neighbour cells that are outside the shape
        outside = get_cell_coordinates(neighbours).difference(shape.inside)
        if outside:
            # mark this piece as an outside element, this will not be a
            # valid piece
            is_outside = True
        # keep the neighbour cells
        neighbours = neighbours.intersection(shape.cells)
        # remove space cells already processed
        neighbours = neighbours.difference(space_cells)
        # save any border cells
        borders = neighbours.difference(shape.space_cells)
        border_cells = border_cells.union(borders)       
        # add neighbour space cells to work queue
        spaces = neighbours.difference(borders)
        piece_q = piece_q.union(spaces)
    return is_outside, border_cells, space_cells

def process_border_cells(cell, shape):
    next_cells = {
        'l': {(-1, 0, 'l'), (-1, 0, 'll'), (1, 0, 'l'), (1, 0, 'ul'), (0, -1, 'r')},
        'r': {(-1, 0, 'r'), (-1, 0, 'lr'), (1, 0, 'r'), (1, 0, 'ur'), (0, 1, 'l')},
        'u': {(0, -1, 'u'), (0, -1, 'ur'), (0, 1, 'u'), (0, 1, 'ul'), (-1, 0, 'd')},
        'd': {(0, -1, 'd'), (0, -1, 'lr'), (0, 1, 'd'), (0, 1, 'll'), (1, 0, 'u')},
        'ul': {(0, -1, 'u'), (0, -1, 'ur'), (-1, 0, 'l'), (-1, 0, 'll'),
               (-1, -1, 'r'), (-1, -1, 'd'), (-1, -1, 'lr')},
        'ur': {(0, 1, 'u'), (0, 1, 'ul'), (-1, 0, 'r'), (-1, 0, 'lr'),
               (-1, 1, 'l'), (-1, 1, 'd'), (-1, 1, 'll')},
        'lr': {(0, 1, 'd'), (0, 1, 'll'), (1, 0, 'r'), (1, 0, 'ur'),
               (1, 1, 'l'), (1, 1, 'u'), (1, 1, 'ul')},
        'll': {(0, -1, 'd'), (0, -1, 'lr'), (1, 0, 'l'), (1, 0, 'ul'),
               (1, -1, 'r'), (1, -1, 'u'), (1, -1, 'ur')},
        }
    is_outside = False
    border_cells = set()
    space_cells = set()
    piece_q = set()
    piece_q.add(cell)
    while piece_q:
        cell = piece_q.pop()
        border_cells.add(cell)
        row, col, cell_type = cell
        # get valid neighbour cells
        valid_neighbours = next_cells[cell_type]
        valid_neighbours = get_absolut_positions(cell, valid_neighbours)
        # test if there are neighbour cells that are outside the shape
        outside = get_cell_coordinates(valid_neighbours).difference(shape.inside)
        if outside:
            # mark this border as an outside element, this will not be a
            # valid piece
            is_outside = True
        # get actual neighbours
        neighbours = valid_neighbours.intersection(shape.border_cells)
        # remove cells that have been processed already
        neighbours = neighbours.difference(border_cells)
        # add border cells to queue for processing
        piece_q = piece_q.union(neighbours)
        # test if space cell is next to the cell
        d_row, d_col = BESIDE[cell_type]
        test_cell = (row + d_row, col + d_col, ' ')
        if test_cell in shape.space_cells:
            space_cells.add(test_cell)
    return is_outside, border_cells, space_cells

def get_cell_coordinates(cells):
    return {(row, col) for row, col, _ in cells}

# def get_neighbours(cell, shape):
#     deltas = {(-1, 0, ' '), (-1, 0, 'd'), (-1, 1, ' '), (-1, 1, 'll'),
#               (0, 1, ' '), (0, 1, 'l'), (1, 1, ' '), (1, 1, 'ul'),
#               (1, 0, ' '), (1, 0, 'u'), (1, -1, ' '), (1, -1, 'ur'),
#               (0, -1, ' '), (0, -1, 'r'), (-1, -1, ' '), (-1, -1, 'lr'),}
#     neighbours = deltas
#     neighbours = get_absolut_positions(cell, neighbours)
#     neighbours = neighbours.intersection(shape.cells)
#     return neighbours

# @Profile(stats=PERFORMANCE_STATS)
def get_pieces_v1(shape):
    main_q = shape.border_cells.copy()
    border_idx = 0
    while main_q:
        cell = main_q.pop()
        border = set()
        main_q, border, attached_spaces, shape = get_one_border(main_q, cell, border_idx, shape)
        if border:
            shape.borders[border_idx] = border
            if attached_spaces:
                shape = add_to_white_space_map(attached_spaces, border_idx, shape)
                shape = add_to_border_map(attached_spaces, border_idx, shape)
            border_idx += 1
    segments = join_segments(shape)
    pieces = join_pieces(shape.borders, segments)
    return pieces

@Profile(stats=PERFORMANCE_STATS)
def add_to_white_space_map(attached_white_spaces, border_idx, shape):
    for white_space in attached_white_spaces:
        if white_space in shape.space_to_borders_map.keys():
            shape.space_to_borders_map[white_space].add(border_idx)                    
        else:
            shape.space_to_borders_map[white_space] = {border_idx}
    return shape

@Profile(stats=PERFORMANCE_STATS)
def add_to_border_map(attached_white_spaces, border_idx, shape):
    if border_idx in shape.border_to_spaces_map.keys():
        shape.border_to_spaces_map[border_idx].add(attached_white_spaces)
    else:
        shape.border_to_spaces_map[border_idx] = attached_white_spaces
    return shape

@Profile(stats=PERFORMANCE_STATS)
def join_segments(shape):
    segments = []
    border_IDs = list(shape.borders.keys())
    while border_IDs:
        border_ID = border_IDs[0]
        segment = set()
        work_q = set()
        work_q.add(border_ID)
        while work_q:
            border_ID = work_q.pop()
            if border_ID in border_IDs:
                border_IDs.remove(border_ID)
            segment.add(border_ID)
            # join border segments that are connected via spaces
            if border_ID in shape.border_to_spaces_map.keys():
                for space in shape.border_to_spaces_map[border_ID]:
                    work_q = work_q.union(shape.space_to_borders_map[space])
            # join border segments that are directly connected
            elif border_ID in shape.border_to_borders_map.keys():
                work_q = work_q.union(shape.border_to_borders_map[border_ID])
            work_q = work_q.difference(segment)                    
        segments.append(segment)
    return segments

@Profile(stats=PERFORMANCE_STATS)
def join_pieces(borders, segments):
    border_IDs = list(borders.keys())
    pieces = []
    for segment in segments:
        piece = set()
        for border_ID in segment:
            piece = piece.union(borders[border_ID])
            border_IDs.remove(border_ID)
        pieces.append(piece)
    for border_ID in border_IDs:
        pieces.append(borders[border_ID])
    return pieces

# @Profile(stats=PERFORMANCE_STATS)
def get_one_border(main_q, cell, border_idx, shape):
    is_a_border = True
    border = set()
    attached_white_spaces = set()
    while cell not in border:
        row, col, cell_type = cell
        # check if cell is outside the shape
        d_row, d_col = BESIDE[cell_type]
        b_pos = (row + d_row, col + d_col)
        if b_pos not in shape.cells.keys():
            is_a_border = False
        # check if beside the cell there is white space
        if b_pos in shape.cell_space_map.keys():
            key = shape.cell_space_map[b_pos]
            attached_white_spaces.add(key)
            if shape.white_spaces[key] == '#':
                is_a_border = False
        # check if beside the cell there is a border element
        if b_pos in shape.cells.keys() and \
            shape.cells[b_pos].intersection({'ul', 'ur', 'll', 'lr', 'r', 'l', 'u', 'd'}):
            # check if the neighbour cell is already part of a border
            if b_pos in shape.cell_border_map.keys():
                key = shape.cell_border_map[b_pos]
                if key in shape.border_to_borders_map.keys():
                    shape.border_to_borders_map[key].add(border_idx)
                else:
                    shape.border_to_borders_map[key] = {border_idx}
                if border_idx in shape.border_to_borders_map.keys():
                    shape.border_to_borders_map[border_idx].add(key)
                else:
                    shape.border_to_borders_map[border_idx] = {key}
        cell, border, main_q, shape = get_next_cell(cell, border_idx,
                                                    border, main_q, shape)
    if not is_a_border:
        border = False
    return main_q, border, attached_white_spaces, shape

# @Profile(stats=PERFORMANCE_STATS)
def get_next_cell(cell, border_idx, border, main_q, shape):
    # get neighbours of current cell
    row, col, cell_type = cell
    neighbours = shape.neighbour_map[(row, col)]
    for n_type, valid_neighbours in NEXT_MAP[cell_type]:
        # add cell to border
        border.add((row, col, n_type))
        # add to cell to border map
        shape.cell_border_map[(row, col)] = border_idx
        # remove processed cell from main queue
        main_q = main_q.difference({(row, col, n_type)})
        # check for valid neighbour cells combination
        neighbour_cells = neighbours.intersection(valid_neighbours)
        if len(neighbour_cells) > 0:
            n_row, n_col, n_cell_type = neighbour_cells.pop()
            cell = (row + n_row, col + n_col, n_cell_type)
            break
    return cell, border, main_q, shape

@Profile(stats=PERFORMANCE_STATS)
def build_neighbour_map(shape):
    """
    Build a dictionary data structure where for each cell (a row, column tuple)
    all neighbouring cells are returned.
    """
    deltas = [(-1, 0), (-1, 1), (0, 1), (1, 1),
              (1, 0), (1, -1), (0, -1), (-1, -1),]
    for row, col in shape.cells:
        neighbour_cells = set()
        for d_row, d_col in deltas:
            n_row, n_col = row + d_row, col + d_col
            if (n_row, n_col) in shape.cells.keys():
                new_set = {(d_row, d_col, cell)
                           for cell in shape.cells[(n_row, n_col)]}
                neighbour_cells = neighbour_cells.union(new_set)
            else:
                neighbour_cells.add((d_row, d_col, '#'))
        shape.neighbour_map[(row, col)] = neighbour_cells
    return shape

@Profile(stats=PERFORMANCE_STATS)
def get_absolut_positions(cell, neighbours):
    """
    Transform relative row, column coordinates into absolute coordinates.
    """
    row, col, _ = cell
    neighbours = {(row + d_row, col + d_col, cell_type)
                  for d_row, d_col, cell_type in neighbours}
    return neighbours

@Profile(stats=PERFORMANCE_STATS)
def set_to_dict(piece):
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+'}    
    dict_piece = {}
    for row, col, cell_type in piece:
        dict_piece[(row, col)] = cell_to_char[cell_type]
    return dict_piece

def plus_to_lines(piece, shape):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    for row, col in piece.keys():
        if piece[(row, col)] == '+':
            piece = should_be_line(row, col, piece, shape)
    return piece

def should_be_line(row, col, piece, shape):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    # TODO: check if this can be optimized and simplified
    vertical = [((-1, 0), '|'), ((-1, 0), '+'), ((1, 0), '|'), ((1, 0), '+'),]
    horizontal = [((0, -1), '-'), ((0, -1), '+'), ((0, 1), '-'), ((0, 1), '+'),]
    horiz_chars = []
    for (d_row, d_col), cell_char in horizontal:
        n_pos = (row + d_row, col + d_col)
        if n_pos in piece.keys() and piece[n_pos] == cell_char:
            horiz_chars.append(cell_char)
    verti_chars = []
    for (d_row, d_col), cell_char in vertical:
        n_pos = (row + d_row, col + d_col)
        if n_pos in piece.keys() and piece[n_pos] == cell_char:
            verti_chars.append(cell_char)
    if len(horiz_chars) == 2 and len(verti_chars) == 0:
        piece[row, col] = '-'
    if len(horiz_chars) == 0 and len(verti_chars) == 2:
        piece[row, col] = '|'
    return piece

# @Profile(stats=PERFORMANCE_STATS)
def plus_to_lines_v1(piece, shape):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    plus_types = {'ul', 'ur', 'lr', 'll'}
    for row, col in piece.keys():
        if plus_types.intersection(piece[(row, col)]):
            piece = should_be_line(row, col, piece, shape)
    return piece

# @Profile(stats=PERFORMANCE_STATS)
def should_be_line_v1(row, col, piece, shape):
    """
    Transform all '+' that are no longer corners or intersections into '|' or
    '-'.
    """
    # TODO: move these up as constants
    next_cells = {
        'ul': {(0, -1, 'u'), (0, -1, 'ur'), (-1, 0, 'l'), (-1, 0, 'll')},
        'ur': {(0, 1, 'u'), (0, 1, 'ul'), (-1, 0, 'r'), (-1, 0, 'lr')},
        'lr': {(0, 1, 'd'), (0, 1, 'll'), (1, 0, 'r'), (1, 0, 'ur')},
        'll': {(0, -1, 'd'), (0, -1, 'lr'), (1, 0, 'l'), (1, 0, 'ul')},
        }
#     horizontal = {
#         (-1, 0, 'l'), (-1, 0, 'r'), (-1, 0, 'lr'), (-1, 0, 'll'),
#         (1, 0, 'l'), (1, 0, 'r'), (1, 0, 'ur'), (1, 0, 'ul'),
#         }
#     vertical = {
#         (0, -1, 'u'), (0, -1, 'd'), (0, -1, 'ur'), (0, -1, 'lr'),
#         (0, 1, 'u'), (0, 1, 'd'), (0, 1, 'ul'), (0, 1, 'll'),
#         }
#     horiz_cells = get_absolut_positions((row, col, ' '), horizontal)
#     horiz_cells = horiz_cells.intersection(shape.border_cells)
#     verti_cells = get_absolut_positions((row, col, ' '), vertical)
#     verti_cells = verti_cells.intersection(shape.border_cells)


    new_cell_types = set()
    cell_types = piece[row, col]
    for cell_type in cell_types:
        adjacent_cells = get_absolut_positions((row, col, cell_type), next_cells[cell_type])
        adjacent_cells = adjacent_cells.intersection(shape.border_cells)
        if len(adjacent_cells) == 1:
            _, _, new_cell_type = adjacent_cells.pop()
            new_cell_types.add(new_cell_type)
    if len(new_cell_types) == 1:
        piece[row, col] = new_cell_types


#     if (row - 1, col) in piece.keys() and \
#         piece[row - 1, col].intersection({'l', 'r', 'll', 'lr'}) and \
#         (row + 1, col) in piece.keys() and \
#         piece[row + 1, col].intersection({'l', 'r', 'ul', 'ur'}) and \
#         ((row, col - 1) not in piece.keys() or \
#         ((row, col - 1) in piece.keys() and \
#          piece[row, col - 1].intersection({'l', 'r'}))) and \
#         ((row, col + 1) not in piece.keys() or \
#         ((row, col + 1) in piece.keys() and \
#          piece[row, col + 1].intersection({'l', 'r'}))):
#         piece[row, col] = {'l', 'r'}
#     elif (row, col - 1) in piece.keys() and \
#         piece[row, col - 1].intersection({'u', 'd', 'ur', 'lr'}) and \
#         (row, col + 1) in piece.keys() and \
#         piece[row, col + 1].intersection({'u', 'd', 'ul', 'll'}) and \
#         ((row - 1, col) not in piece.keys() or \
#         ((row - 1, col) in piece.keys() and \
#          piece[row - 1, col].intersection({'u', 'd'}))) and \
#         ((row + 1, col) not in piece.keys() or \
#         ((row + 1, col) in piece.keys() and \
#          piece[row + 1, col].intersection({'u', 'd'}))):
#         piece[row, col] = {'u', 'd'}

    return piece

@Profile(stats=PERFORMANCE_STATS)
def piece_to_text_lines(piece, shape):
    """
    Transform the piece matrix into a list of text lines.
    """
    shape_txt = shape.blank_lines[:]
    for row, col in piece.keys():
        cell = piece[(row, col)]
        shape_txt[row] = shape_txt[row][:col] + cell + shape_txt[row][col + 1:]
    return shape_txt

@Profile(stats=PERFORMANCE_STATS)
def piece_to_text_lines_v1(piece, shape):
    """
    Transform the piece matrix into a list of text lines.
    """
    cell_to_char = {' ': ' ', 'u': '-', 'd': '-', 'l': '|', 'r': '|',
                    'ul': '+', 'ur': '+', 'lr': '+', 'll': '+'}
    shape_txt = shape.blank_lines[:]
    for row, col in piece.keys():
        cell = piece[(row, col)].pop()
        shape_txt[row] = shape_txt[row][:col] + cell_to_char[cell] + shape_txt[row][col + 1:]
    return shape_txt

@Profile(stats=PERFORMANCE_STATS)
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
+-+
| |
| +--+
|  +-+
|  |
+--+
""".strip('\n')

#     INPUT_SHAPE = """
# +-+
# | |
# | +--+
# |  +-+
# |  |
# |  +-+
# +----+
# """.strip('\n')

#     INPUT_SHAPE = """
# +--------+-+----------------+-+----------------+-+--------+
# |        | |                | |                | |        |
# |        ++++               | |                | |        |
# |        ++++               | |                | |        |
# |        ++++             +-+ +-+            +-+ +-+      |
# |        ++++             |     |            |     |      |
# +-----------+      +------+     +------------+     +------+
# | +--------+|      |                                      |
# +-+   +---+||      +--------------------------------------+
# |     |+-+|||                                             |
# |     || ++||                                             |
# |     |+---+|                                             |
# |     +-----+                                             |
# |        +-+                +-+                +-+        |
# |        +-+                | |                | |        |
# |    +------+               | |                | |        |
# |    |+----+|         +-----+ |                | |        |
# |    ||+--+||         |+-+    |              +-+ +-+      |
# |    |||++|||         || |  +-+              |     |      |
# ++   |||++|||      +--+| +--+    +-----------+     +------+
# ||   |||+-+||      |   |      +--+                        |
# ++   ||+---+|      +---+  +---+   +-----------------------+
# |    |+-++--+             |       |                       |
# |+---+--+|                +-+ +---+                       |
# |+-------+                  | |                           |
# |                           | |                           |
# |        +-+                | |                +-+        |
# |        +-+                +-+                +-+        |
# |                       +------+                          |
# |                       |+----+|                          |
# |                       ||+--+||                          |
# |       +----+          |||++|||                          |
# ++      |+--+|  ++--+   |||++|||      +-------------------+
# ||      ||++||  ||  |   |||+-+||      |                   |
# ++      ||++||  ++--+   ||+---+|      +------+     +------+
# |       |+--+|          |+-++--+             |     |      |
# |       +----+      +---+--+|                +-+ +-+      |
# |                   +-------+                  | |        |
# |                                              | |        |
# |        +-+                +-+                | |        |
# |        +-+                +-+                +-+        |
# |  +-----+ |    ++                                        |
# |  +-++----+    ++                                        |
# |    ++                                                   |
# |    ||                                                   |
# ++   |+-------------+                 +-------------------+
# ||   |              |                 |                   |
# ++   +---+ +--------+                 +------+     +------+
# |        | |                                 |     |      |
# |        | |                                 +-+ +-+      |
# |        | |                                   | |        |
# |        | |                                   | |        |
# |        | |                +-+                | |        |
# |        +-+                | |                | |        |
# |  +-----+ |    ++          | |                | |        |
# |  +-++----+    ++    +-----+ |                | +-----+  |
# |    ++               |+-+    |                |    +-+|  |
# |    ||               || |  +-+                +-+  | ||  |
# ++   |+---------------+| +--+    +----------+    +--+ |+--+
# ||   |                 |      +--+          +--+      |   |
# ++   +---+ +-----------+  +---+   +--------+   +---+  +---+
# |        | |              |       |        |       |      |
# |        | |              +-+ +---+        +---+ +-+      |
# |        | |                | |                | |        |
# |        | |                | |                | |        |
# |        | |                | |                | |        |
# +--------+-+----------------+-+----------------+-+--------+
# """.strip('\n')

    ALL_PIECES = break_evil_pieces(INPUT_SHAPE)
    with open('break_the_pieces_evilized_edition.csv', 'w') as outfile:
        outfile.write('{}; {}\n'.format('function', 'time'))
        for entry in PERFORMANCE_STATS:
            text_line = ' '.join(['{};'.format(item) for item in entry]) + '\n'
            outfile.write(text_line)
    for counter, text_piece in enumerate(ALL_PIECES):
        print('\n{}.) piece:\n'.format(counter))
        print(text_piece)
    print()
