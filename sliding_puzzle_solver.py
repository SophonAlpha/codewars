import pprint
from itertools import cycle

def slide_puzzle(ar):
    sequence = None
    for t in range(1, len(ar)**2):
        pprint.pprint(ar) # debug
        print() # debug
        move_tile_to_target(t, ar)
    return sequence

def get_position(t, ar):
    row, col = [(i, row.index(t)) for i, row in enumerate(ar) if t in row][0]
    return row, col

def get_target_position(t, ar):
    n = len(ar)
    row = int(t / n)
    col = (t % n) - 1
    if col == -1: 
        row = int(t / n) - 1
        col = n - 1
    return row, col

def get_surrounding_tiles(t, ar):
    positions = [(-1, 0), (-1, 1), (0, 1), ( 1,  1), 
                 ( 1, 0), ( 1,-1), (0,-1), (-1, -1)]
    t_row, t_col = get_position(t, ar)
    n = len(ar)
    sequence = []
    for d_row, d_col in positions:
        check_row = t_row + d_row
        check_col = t_col + d_col
        if check_row >= 0 and check_row <= n and \
           check_col >= 0 and check_col <= n:
            sequence.append(ar[check_row][check_col])
        else:
            sequence.append(None)
    return sequence

def move_empty_next_to_tile(t, ar):
    # initialise
    empty_row, empty_col = get_position(0, ar)
    tile_row, tile_col = get_position(t, ar)
    # move along columns
    while abs((tile_col - empty_col)) > 1:
        col_step = 1 if (tile_col - empty_col) > 1 else -1
        tile_to_move = empty_row, empty_col + col_step
        ar = move_tile(tile_to_move, ar)
        # update after tile move
        empty_row, empty_col = get_position(0, ar)
        tile_row, tile_col = get_position(t, ar)
    # move along rows
    while abs((tile_row - empty_row)) > 1:
        row_step = 1 if (tile_row - empty_row) > 1 else -1
        tile_to_move = empty_row + row_step, empty_col
        ar = move_tile(tile_to_move, ar)
        # update after tile move
        empty_row, empty_col = get_position(0, ar)
        tile_row, tile_col = get_position(t, ar)
    return ar

def move_tile_to_target(t, ar):
    t_row, t_col = get_target_position(t, ar)
    c_row, c_col = get_position(t, ar)
    while not(c_row == t_row and c_col == t_col):
        surrounding_tiles = get_surrounding_tiles(t, ar)
        if not(0 in surrounding_tiles):
            ar = move_empty_next_to_tile(t, ar)
            surrounding_tiles = get_surrounding_tiles(t, ar)
        sequence = get_sequence(surrounding_tiles,
                                t_row, t_col,
                                c_row, c_col)
        sequence.append(t)
        for tile in sequence:
            ar = move_tile(tile, ar)
        c_row, c_col = get_position(t, ar)
    return ar

def get_sequence(surrounding_tiles, t_row, t_col, c_row, c_col):
    start = surrounding_tiles.index(0)
    if t_row - c_row > 0: # move down
        stop = 4
    if t_row - c_row < 0: # move up
        stop = 0
    if t_col - c_col > 0: # move right
        stop = 2
    if t_col - c_col < 0: # move left
        stop = 6
    direction =  1 if abs(start - stop) > 3 and not(None in surrounding_tiles[start:]) else -1
    sequence = []
    c = start
    while True:
        i = c % len(surrounding_tiles)
        sequence.append(surrounding_tiles[i])
        if i == stop:
            break
        else:
            c = c + direction
    return sequence[1:] # drop the empty tile

def move_tile(tile_to_move, ar):
    empty_row, empty_col = get_position(0, ar)
    a = type(tile_to_move)
    if isinstance(tile_to_move, tuple):
        tile_row, tile_col = tile_to_move
    else:
        tile_row, tile_col = get_position(tile_to_move, ar)
    # check that empty tile is next to tile to move
    if (abs(tile_row - empty_row) == 1 and \
        abs(tile_col - empty_col) == 0) or\
       (abs(tile_row - empty_row) == 0 and \
        abs(tile_col - empty_col) == 1):
        ar[empty_row][empty_col] = ar[tile_row][tile_col]
        ar[tile_row][tile_col] = 0
    else:
        print('Cannot move. Tile is not next to empty tile.')
    return ar

puzzle = [
    [ 3, 7,14,15,10],
    [ 1, 0, 5, 9, 4],
    [16, 2,11,12, 8],
    [17, 6,13,18,20],
    [21,22,23,19,24] ]
puzzle = [
    [17, 9, 6,11, 5],
    [22,13, 7,18,20],
    [ 8,16, 2,12,15],
    [ 1,24,10, 3, 4],
    [21,23,19, 0,14] ]

print(slide_puzzle(puzzle))
