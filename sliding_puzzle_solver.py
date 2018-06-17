import pprint

do_not_move = {}

def slide_puzzle(ar):
    n = len(ar)
    global do_not_move
    do_not_move = {tile: False for tile in range(0, n**2)}
    for i in range(0, n - 1):
        row, col = get_row_column_tiles(i, n)
        # move tiles in row, except the last two, to target position
        for tile in row[:-2]:
            target_row, target_col = get_target_position(tile, ar)
            ar = move_tile_to_target(tile, target_row, target_col, ar)
            do_not_move[tile] = True
        # move last two tiles in row to intermediate position
        # first we move the last tile of the row to the lower right corner
        # as a precaution to avoid it getting "stuck" with the before last tile
        before_last_tile = row[-2:-1][0]
        last_tile = row[-1:  ][0]
        ar = move_tile_to_target(last_tile, n - 1, n - 1, ar)
        # the we move the before last tile to its intermediate position
        ar = move_tile_to_target(before_last_tile,i, n - 1, ar)
        do_not_move[before_last_tile] = True
        # then the last tile to its intermediate position
        ar = move_tile_to_target(last_tile, i + 1, n - 1, ar)
        do_not_move[last_tile] = True
        # "turn" last two tiles in row from intermediate to final positions
        ar = turn_last_two_tiles([before_last_tile, last_tile], ar)
        pprint.pprint(ar)

#        print(col[:-2])
        tile = col[-2:-1]
        target_row = n - 1
        target_col = i
#        print('{} --> {}, {}'.format(tile, target_row, target_col))
        tile = col[-1:]
        target_row = n - 1
        target_col = i + 1
#        print('{} --> {}, {}'.format(tile, target_row, target_col))
                
    return

def turn_last_two_tiles(tiles, ar):
    for tile in tiles:
        target_row, target_col = get_target_position(tile, ar)
        ar = move_tile_to_target(tile, target_row, target_col, ar)
        do_not_move[tile] = True
    return ar

def get_row_column_tiles(i, n):
    # sort the row
    start = 1 + i * n + i
    stop = (i + 1) * n + 1
    row = [tile for tile in range(start, stop)]
    # sort the column
    start = (i + 1) * n + ((i + 1) * 1)
    stop = n**2
    step = n
    col = [tile for tile in range(start ,stop, step)]
    return row, col

def slide_puzzle_v2(ar):
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
    n = len(ar) - 1
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
    closest_tile_row, closest_tile_col = get_position(closest_tile(t, ar), ar)
    while abs((closest_tile_col - empty_col)) > 0 or \
          abs((closest_tile_row - empty_row)) > 0:
        # move along columns
        if not(closest_tile_col - empty_col == 0):
            col_step = 1 if (closest_tile_col - empty_col) > 1 else -1
            tile_to_move = empty_row, empty_col + col_step
            if not(do_not_move[ar[tile_to_move[0]][tile_to_move[1]]]):
                ar = move_tile(tile_to_move, ar)
        # move along rows
        elif not(closest_tile_row - empty_row == 0):
            row_step = 1 if (closest_tile_row - empty_row) > 1 else -1
            tile_to_move = empty_row + row_step, empty_col
            if not(do_not_move[ar[tile_to_move[0]][tile_to_move[1]]]):
                ar = move_tile(tile_to_move, ar)
        # update after tile move
        empty_row, empty_col = get_position(0, ar)
        closest_tile_row, closest_tile_col = get_position(closest_tile(t, ar), ar)
    return ar

def closest_tile(t, ar):
    empty_row, empty_col = get_position(0, ar)
    surrounding_tiles = get_surrounding_tiles(t, ar)
    closest_tile = 0
    distance = len(ar)**2
    for tile in surrounding_tiles:
        if not(tile == None):
            tile_row, tile_col = get_position(tile, ar)
            d = abs(tile_row - empty_row) + abs(tile_col - empty_col)
            if distance > d:
                distance = d
                closest_tile = tile
    return closest_tile

def move_tile_to_target(t, t_row, t_col, ar):
    c_row, c_col = get_position(t, ar)
    while not(c_row == t_row and c_col == t_col):
        surrounding_tiles = get_surrounding_tiles(t, ar)
        if not(0 in surrounding_tiles):
            ar = move_empty_next_to_tile(t, ar)
        sequence = get_sequence(t, t_row, t_col, ar)
        for tile in sequence:
            ar = move_tile(tile, ar)
        c_row, c_col = get_position(t, ar)
    return ar

def get_sequence(t, t_row, t_col, ar):
#    if is_last_in_row(t, ar):
#        sequence = get_last_in_row_sequence(t, ar)
#    else:
    c_row, c_col = get_position(t, ar)
    surrounding_tiles = get_surrounding_tiles(t, ar)
    start = surrounding_tiles.index(0)
    if t_row - c_row > 0: # move down
        stop = 4
    if t_row - c_row < 0: # move up
        stop = 0
    if t_col - c_col > 0: # move right
        stop = 2
    if t_col - c_col < 0: # move left
        stop = 6
    # mark with 'None' all tiles that are already on their target position
    surrounding_tiles = [tile \
                         if (not(tile == None) and not(do_not_move[tile])) or tile == 0 else None \
                         for tile in surrounding_tiles]
    # build sequence of tiles to move
    if start - stop > 0:
        direction =  1 if abs(start - stop) > 3 and not(None in surrounding_tiles[start + 1:]) else -1
    if start - stop < 0:
        direction =  1 if abs(start - stop) < 5 and not(None in surrounding_tiles[start:stop + 1]) else -1
    sequence = []
    c = start
    while True:
        i = c % len(surrounding_tiles)
        sequence.append(surrounding_tiles[i])
        if i == stop:
            break
        else:
            c = c + direction
    sequence = sequence[1:] + [t]
    return sequence

def is_last_in_row(t, ar):
    t_row, t_col = get_target_position(t, ar)
    c_row, c_col = get_position(t, ar)
    if c_col == len(ar) - 1 and c_row == t_row + 1:
        return True
    return False

def get_last_in_row_sequence(t, ar):
    c_row, c_col = get_position(t, ar)
    surrounding_tiles = get_surrounding_tiles(t, ar)
    if surrounding_tiles[0] == 0:
        # empty tile is already at target position
        sequence = [t]
        return sequence
    # add the tiles around the tile to be moved
    start = surrounding_tiles.index(0)
    sequence = surrounding_tiles[start + 1:6 + 1]
    # add the tiles in the row below the target row from right to left
    sequence = sequence[:] + ar[c_row][c_col - 2::-1]
    # add the tiles in the target row from left to right
    target_row = ar[c_row - 1]
    sequence = sequence[:] + target_row
    # tile to target position
    sequence = sequence[:] + [t]
    # restore target row
    sequence = sequence[:] + [ar[c_row][c_col - 2]] + [ar[c_row - 1][c_col]] + target_row[-2::-1]
    return sequence

def move_tile(tile_to_move, ar):
    empty_row, empty_col = get_position(0, ar)
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
puzzle = [
    [ 7,18,22, 2, 5],
    [12, 6, 3, 0, 9],
    [ 1, 8,17, 4,15],
    [19,21,14,10,20],
    [16,23,13,11,24] ]


print(slide_puzzle(puzzle))
