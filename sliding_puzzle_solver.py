import pprint
import math
from itertools import cycle
from itertools import islice

# A tile marked as 'untouchable' cannot be moved when the empty
# tile moves around. However, a tile can still be moved directly when the
# empty tile is right next to it.
untouchable = {}

def slide_puzzle(tile_array):
    """
    The puzzle solver function. Takes a tile puzzle as input and resolves it
    applying the algorithm outlined here: https://www.giantbomb.com/
    sliding-block-puzzles/3030-34998/forums/
    a-fool-proof-guide-to-solving-every-solvable-slidi-1802039/
    """
    puzzle_size = len(tile_array)
    global untouchable
    untouchable = {tile: False for tile in range(0, puzzle_size**2)}
    # solve rows and columns
    for size in range(0, puzzle_size - 2):
        row_tiles, col_tiles = get_first_row_first_column_tiles(size, puzzle_size)
        tile_array = solve_tiles(row_tiles, tile_array, 'row', size, puzzle_size)
        tile_array = solve_tiles(col_tiles, tile_array, 'col', size, puzzle_size)
    # solve the remaining 2x2 tiles in the lower right corner
    tile_array = solve_2x2(tile_array)
    pprint.pprint(tile_array)
    return

def solve_tiles(tiles, tile_array, direction, size, puzzle_size):
    intermediate_pos = {'row': [(size, puzzle_size - 1),
                                (size + 1, puzzle_size - 1)],
                        'col': [(puzzle_size - 1, size),
                                (puzzle_size - 1, size + 1)]}
    # move tiles, except the last two, to target position
    for tile in tiles[:-2]:
        target_row, target_col = get_target_position(tile, tile_array)
        tile_array = move_tile_to_target(tile, target_row, target_col, tile_array)
    # Move last two tiles in row_tiles to intermediate positions.
    # First we move the last tile of the row_tiles to the lower right corner
    # as a precaution to avoid blocking in the before last tile
    before_last_tile = tiles[-2:-1][0]
    last_tile = tiles[-1:][0]
    tile_array = move_tile_to_target(last_tile, puzzle_size - 1, puzzle_size - 1, tile_array)
    # Then we move the before last tile to its intermediate position.
    tile_array = move_tile_to_target(before_last_tile,
                                     intermediate_pos[direction][0][0],
                                     intermediate_pos[direction][0][1],
                                     tile_array)
    # Then the last tile to its intermediate position
    tile_array = move_tile_to_target(last_tile,
                                     intermediate_pos[direction][1][0],
                                     intermediate_pos[direction][1][1],
                                     tile_array)
    # "Turn" last two tiles in row_tiles from intermediate to final positions.
    tile_array = turn_last_two_tiles([before_last_tile, last_tile], tile_array)
    return tile_array

def solve_2x2(tile_array):
    puzzle_size = len(tile_array)
    # create a circular list of position deltas that starts at the empty tile
    positions = [(0, 0), (-1, 0), (-1, -1), (0, -1)]
    empty_tile_row, empty_tile_col = get_position(0, tile_array)    
    d_row = empty_tile_row - (puzzle_size - 1)
    d_col = empty_tile_col - (puzzle_size - 1)
    start = positions.index((d_row, d_col))
    positions = cycle(positions)
    positions = islice(positions, start, None)
    # move to next position
    next(positions)
    # move to each position and check if we are finished
    for _ in range(3):
        d_row, d_col = next(positions)
        tile = tile_array[puzzle_size - 1 + d_row][puzzle_size - 1 + d_col]
        tile_array = move_tile(tile, tile_array)
        if is_puzzle_solved(tile_array):
            break
    return tile_array

def is_puzzle_solved(tile_array):
    puzzle_size = len(tile_array)
    solved_puzzle = []
    tile_number = 1
    for _ in range(puzzle_size):
        solved_puzzle.append([tile_number + i for i in range(puzzle_size)])
        tile_number += puzzle_size
    solved_puzzle[puzzle_size -1][puzzle_size -1] = 0
    return tile_array == solved_puzzle
        

def turn_last_two_tiles(tiles, tile_array):
    for tile in tiles:
        target_row, target_col = get_target_position(tile, tile_array)
        tile_array = move_tile_to_target(tile, target_row, target_col, tile_array)
        untouchable[tile] = True
    return tile_array

def get_first_row_first_column_tiles(size, puzzle_size):
    # sort the row_tiles
    start = 1 + size * puzzle_size + size
    stop = (size + 1) * puzzle_size + 1
    row_tiles = [tile for tile in range(start, stop)]
    # sort the column
    start = (size + 1) * puzzle_size + ((size + 1) * 1)
    stop = puzzle_size**2
    step = puzzle_size
    col_tiles = [tile for tile in range(start, stop, step)]
    return row_tiles, col_tiles

def get_position(tile, tile_array):
    """
    For a given tile, return the position as row and column in the puzzle.
    """
    row, col = [(i, row.index(tile))
                for i, row in enumerate(tile_array) if tile in row][0]
    return row, col

def get_target_position(tile, tile_array):
    puzzle_size = len(tile_array)
    row = int(tile / puzzle_size)
    col = (tile % puzzle_size) - 1
    if col == -1:
        row = int(tile / puzzle_size) - 1
        col = puzzle_size - 1
    return row, col

def get_surrounding_tiles(tile, tile_array):
    positions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    t_row, t_col = get_position(tile, tile_array)
    puzzle_size = len(tile_array)
    sequence = []
    for d_row, d_col in positions:
        check_row = t_row + d_row
        check_col = t_col + d_col
        if check_row >= 0 and check_row <= puzzle_size - 1 and \
           check_col >= 0 and check_col <= puzzle_size - 1:
            sequence.append(tile_array[check_row][check_col])
        else:
            sequence.append(None)
    return sequence

def move_tile_to_target(tile, t_row, t_col, tile_array):
    c_row, c_col = get_position(tile, tile_array)
    untouchable[tile] = True
    while not(c_row == t_row and c_col == t_col):
        n_row, n_col = get_next_position(tile, t_row, t_col, tile_array)
        tile_array = move_empty_to_position(n_row, n_col, tile_array)
        tile_array = move_tile(tile, tile_array)
        c_row, c_col = get_position(tile, tile_array)
    return tile_array

def get_next_position(tile, t_row, t_col, tile_array):
    possible_positions = get_all_possible_positions(tile, tile_array)
    next_position = get_position_closest_to_target(possible_positions,
                                                   t_row, t_col, tile_array)
    return next_position

def get_all_possible_positions(tile, tile_array):
    puzzle_size = len(tile_array)
    c_row, c_col = get_position(tile, tile_array)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    possible_positions = []
    for d_row, d_col in directions:
        n_row = c_row + d_row
        n_col = c_col + d_col
        if (0 <= n_row <= puzzle_size - 1) and \
           (0 <= n_col <= puzzle_size - 1) and \
           not untouchable[tile_array[n_row][n_col]]:
            possible_positions.append((n_row, n_col))
    return possible_positions

def get_position_closest_to_target(possible_positions, t_row, t_col, tile_array):
    puzzle_size = len(tile_array)
    distance = puzzle_size**2 # initialisation with high value
    for n_row, n_col in possible_positions:
        n_distance = math.sqrt(abs(t_row - n_row)**2 + abs(t_col - n_col)**2)
        if n_distance < distance:
            next_position = (n_row, n_col)
            distance = n_distance
    return next_position

def move_empty_to_position(t_row, t_col, tile_array):
    sequence = get_shortest_path(0, t_row, t_col, tile_array)
    for tile in sequence:
        tile_array = move_tile(tile, tile_array)
    return tile_array

def get_shortest_path(start_tile, target_row, target_col, tile_array):
    graph = build_graph(start_tile, tile_array)
    distances = calculate_distances(start_tile, graph)
    tile_sequence = get_shortest_tile_sequence(distances, graph, start_tile,
                                               target_row, target_col, tile_array)
    tile_sequence.reverse()
    return tile_sequence

def build_graph(start_tile, tile_array):
    num_tiles = len(tile_array)**2
    distance = 1 # distance for all tiles
    graph = {}
    for tile in range(0, num_tiles):
        if not untouchable[tile]:
            surrounding_tiles = get_surrounding_tiles(tile, tile_array)
            graph[tile] = {start_tile:distance for start_tile in surrounding_tiles \
                           if not(start_tile is None) and not untouchable[start_tile]}
    return graph

def calculate_distances(start_tile, graph):
    # based on this introduction to the Dijkstra algorithm:
    # https://brilliant.org/wiki/dijkstras-short-path-finder/
    infinity = float('inf')
    unvisited = [vertex for vertex in graph if not untouchable[vertex]]
    distances = {vertex: infinity for vertex in unvisited}
    distances[start_tile] = 0
    # calculate distances from source
    while unvisited:
        unvisited_dist = {v:distances[v] for v in unvisited}
        vertex = min(unvisited_dist, key=unvisited_dist.get)
        unvisited.remove(vertex)
        for neighbor in graph[vertex]:
            alt = distances[vertex] + graph[vertex][neighbor]
            if alt < distances[neighbor]:
                distances[neighbor] = alt
    return distances

def get_shortest_tile_sequence(distances, graph, start_tile, target_row, target_col, tile_array):
    tile = tile_array[target_row][target_col]
    tile_sequence = []
    while not tile == start_tile:
        neighbor_dist = {neighbor:distances[neighbor] for neighbor in graph[tile]}
        tile_sequence.append(tile)
        tile = min(neighbor_dist, key=neighbor_dist.get)
    return tile_sequence

def move_tile(tile_to_move, tile_array):
    """
    Move a tile. The empty tile needs to be next to it.
    """
    empty_row, empty_col = get_position(0, tile_array)
    if isinstance(tile_to_move, tuple):
        tile_row, tile_col = tile_to_move
    else:
        tile_row, tile_col = get_position(tile_to_move, tile_array)
    # check that empty tile is next to tile to move
    if (abs(tile_row - empty_row) == 1 and \
        abs(tile_col - empty_col) == 0) or\
       (abs(tile_row - empty_row) == 0 and \
        abs(tile_col - empty_col) == 1):
        tile_array[empty_row][empty_col] = tile_array[tile_row][tile_col]
        tile_array[tile_row][tile_col] = 0
    else:
        print('Cannot move. Tile is not next to empty tile.')
    return tile_array

PUZZLE = [
    [3, 7, 14, 15, 10],
    [1, 0, 5, 9, 4],
    [16, 2, 11, 12, 8],
    [17, 6, 13, 18, 20],
    [21, 22, 23, 19, 24]]
PUZZLE = [
    [17, 9, 6, 11, 5],
    [22, 13, 7, 18, 20],
    [8, 16, 2, 12, 15],
    [1, 24, 10, 3, 4],
    [21, 23, 19, 0, 14]]
PUZZLE = [
    [7, 18, 22, 2, 5],
    [12, 6, 3, 0, 9],
    [1, 8, 17, 4, 15],
    [19, 21, 14, 10, 20],
    [16, 23, 13, 11, 24]]

print(slide_puzzle(PUZZLE))
