import pprint
import math

def slide_puzzle(tile_array):
    """
    main function, does setup and solves the puzzle
    """
    puzzle = SlindingPuzzle(tile_array)
    ret = puzzle.solve()
    return ret

class SlindingPuzzle:
    
    def __init__(self, tile_array):
        self.tile_array = tile_array
        self.puzzle_size = len(tile_array)
        self.untouchable = {tile: False for tile in range(0, self.puzzle_size**2)}
        self.solved_puzzle = self.create_solved_puzzle()
        self.solution_seq = []
        
    def create_solved_puzzle(self):
        solved_puzzle = []
        tile_number = 1
        for _ in range(self.puzzle_size):
            solved_puzzle.append([tile_number + i for i in range(self.puzzle_size)])
            tile_number += self.puzzle_size
        solved_puzzle[self.puzzle_size -1][self.puzzle_size -1] = 0
        return solved_puzzle

    def solve(self):
        """
        The puzzle solver function. Takes a tile puzzle as input and resolves it
        applying the algorithm outlined here: https://www.giantbomb.com/
        sliding-block-puzzles/3030-34998/forums/
        a-fool-proof-guide-to-solving-every-solvable-slidi-1802039/
        """
        # solve rows and columns
        for size in range(0, self.puzzle_size - 1):
            row_tiles, col_tiles = self.get_first_row_first_column_tiles(size)
            self.solve_tiles(row_tiles, 'row', size)
            if self.tile_array == self.solved_puzzle:
                break
            self.solve_tiles(col_tiles, 'col', size)
            if self.tile_array == self.solved_puzzle:
                break
        return self.solution_seq

    def solve_tiles(self, tiles, direction, size):
        intermediate_pos = {'row': [(size, self.puzzle_size - 1),
                                    (size + 1, self.puzzle_size - 1)],
                            'col': [(self.puzzle_size - 1, size),
                                    (self.puzzle_size - 1, size + 1)]}
        # move tiles, except the last two, to target position
        for tile in tiles[:-2]:
            target_row, target_col = self.get_target_position(tile)
            self.move_tile_to_target(tile, target_row, target_col)
        # Move last two tiles in row_tiles to intermediate positions.
        # First we move the last tile of the row_tiles to the lower right corner
        # as a precaution to avoid blocking in the before last tile
        before_last_tile = tiles[-2:-1][0]
        last_tile = tiles[-1:][0]
        self.move_tile_to_target(last_tile, self.puzzle_size - 1, self.puzzle_size - 1)
        self.untouchable[last_tile] = False
        # Then we move the before last tile to its intermediate position.
        self.move_tile_to_target(before_last_tile,
                                 intermediate_pos[direction][0][0],
                                 intermediate_pos[direction][0][1])
        # Then the last tile to its intermediate position
        self.move_tile_to_target(last_tile,
                                 intermediate_pos[direction][1][0],
                                 intermediate_pos[direction][1][1])
        # "Turn" last two tiles in row_tiles from intermediate to final positions.
        self.turn_last_two_tiles([before_last_tile, last_tile])
        return

    def turn_last_two_tiles(self, tiles):
        for tile in tiles:
            target_row, target_col = self.get_target_position(tile)
            self.move_tile_to_target(tile, target_row, target_col)
            self.untouchable[tile] = True
        return

    def get_first_row_first_column_tiles(self, size):
        # sort the row_tiles
        start = 1 + size * self.puzzle_size + size
        stop = (size + 1) * self.puzzle_size + 1
        row_tiles = [tile for tile in range(start, stop)]
        # sort the column
        start = (size + 1) * self.puzzle_size + ((size + 1) * 1)
        stop = self.puzzle_size**2
        step = self.puzzle_size
        col_tiles = [tile for tile in range(start, stop, step)]
        return row_tiles, col_tiles

    def get_target_position(self, tile):
        row = int(tile / self.puzzle_size)
        col = (tile % self.puzzle_size) - 1
        if col == -1:
            row = int(tile / self.puzzle_size) - 1
            col = self.puzzle_size - 1
        return row, col

    def move_tile_to_target(self, tile, t_row, t_col):
        c_row, c_col = self.get_position(tile)
        self.untouchable[tile] = True
        while not(c_row == t_row and c_col == t_col):
            n_row, n_col = self.get_next_position(tile, t_row, t_col)
            self.move_empty_to_position(n_row, n_col)
            self.move_tile(tile)
            c_row, c_col = self.get_position(tile)
        return self.tile_array

    def get_next_position(self, tile, t_row, t_col):
        possible_positions = self.get_all_possible_positions(tile)
        next_position = self.get_position_closest_to_target(possible_positions,
                                                            t_row, t_col)
        return next_position

    def get_all_possible_positions(self, tile):
        c_row, c_col = self.get_position(tile)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        possible_positions = []
        for d_row, d_col in directions:
            n_row = c_row + d_row
            n_col = c_col + d_col
            if (0 <= n_row <= self.puzzle_size - 1) and \
               (0 <= n_col <= self.puzzle_size - 1) and \
               not self.untouchable[self.tile_array[n_row][n_col]]:
                possible_positions.append((n_row, n_col))
        return possible_positions

    def get_position_closest_to_target(self, possible_positions, t_row, t_col):
        distance = self.puzzle_size**2 # initialisation with high value
        for n_row, n_col in possible_positions:
            n_distance = math.sqrt(abs(t_row - n_row)**2 + abs(t_col - n_col)**2)
            if n_distance < distance:
                next_position = (n_row, n_col)
                distance = n_distance
        return next_position

    def move_empty_to_position(self, t_row, t_col):
        sequence = self.get_shortest_path(0, t_row, t_col)
        for tile in sequence:
            self.move_tile(tile)
        return

    def get_shortest_path(self, start_tile, target_row, target_col):
        graph = self.build_graph(start_tile)
        distances = self.calculate_distances(start_tile, graph)
        tile_sequence = self.get_shortest_tile_sequence(distances,graph,
                                                        start_tile,
                                                        target_row, target_col)
        tile_sequence.reverse()
        return tile_sequence

    def build_graph(self, start_tile):
        num_tiles = len(self.tile_array)**2
        distance = 1 # distance for all tiles
        graph = {}
        for tile in range(0, num_tiles):
            if not self.untouchable[tile]:
                surrounding_tiles = self.get_surrounding_tiles(tile)
                graph[tile] = {start_tile:distance for start_tile in surrounding_tiles \
                               if not(start_tile is None) and not self.untouchable[start_tile]}
        return graph

    def calculate_distances(self, start_tile, graph):
        # based on this introduction to the Dijkstra algorithm:
        # https://brilliant.org/wiki/dijkstras-short-path-finder/
        infinity = float('inf')
        unvisited = [vertex for vertex in graph if not self.untouchable[vertex]]
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

    def get_shortest_tile_sequence(self, distances, graph, start_tile,
                                   target_row, target_col):
        tile = self.tile_array[target_row][target_col]
        tile_sequence = []
        while not tile == start_tile:
            neighbor_dist = {neighbor:distances[neighbor] for neighbor in graph[tile]}
            tile_sequence.append(tile)
            tile = min(neighbor_dist, key=neighbor_dist.get)
        return tile_sequence

    def get_position(self, tile):
        """
        For a given tile, return the position as row and column in the puzzle.
        """
        row, col = [(i, row.index(tile))
                    for i, row in enumerate(self.tile_array) if tile in row][0]
        return row, col

    def get_surrounding_tiles(self, tile):
        positions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        t_row, t_col = self.get_position(tile)
        sequence = []
        for d_row, d_col in positions:
            check_row = t_row + d_row
            check_col = t_col + d_col
            if check_row >= 0 and check_row <= self.puzzle_size - 1 and \
               check_col >= 0 and check_col <= self.puzzle_size - 1:
                sequence.append(self.tile_array[check_row][check_col])
            else:
                sequence.append(None)
        return sequence

    def move_tile(self, tile_to_move):
        """
        Move a tile. The empty tile needs to be next to it.
        """
        empty_row, empty_col = self.get_position(0)
        if isinstance(tile_to_move, tuple):
            tile_row, tile_col = tile_to_move
        else:
            tile_row, tile_col = self.get_position(tile_to_move)
        # check that empty tile is next to tile to move
        if (abs(tile_row - empty_row) == 1 and \
            abs(tile_col - empty_col) == 0) or\
           (abs(tile_row - empty_row) == 0 and \
            abs(tile_col - empty_col) == 1):
            self.solution_seq.append(self.tile_array[tile_row][tile_col])
            self.tile_array[empty_row][empty_col] = self.tile_array[tile_row][tile_col]
            self.tile_array[tile_row][tile_col] = 0
        else:
            print('Cannot move. Tile is not next to empty tile.')
        return

PUZZLE = [
    [4, 1, 5],
    [3, 0, 8],
    [7, 6, 2]]
pprint.pprint(PUZZLE)
print(slide_puzzle(PUZZLE))
PUZZLE = [
    [11, 0, 7, 3],
    [2, 1, 5, 4],
    [13, 10, 6, 15],
    [14, 12, 8, 9]]
pprint.pprint(PUZZLE)
print(slide_puzzle(PUZZLE))
PUZZLE = [
    [6, 5, 12, 9],
    [10, 8, 1, 2],
    [14, 0, 4, 3],
    [13, 7, 11, 15]]
pprint.pprint(PUZZLE)
print(slide_puzzle(PUZZLE))
PUZZLE = [
    [3, 7, 14, 15, 10],
    [1, 0, 5, 9, 4],
    [16, 2, 11, 12, 8],
    [17, 6, 13, 18, 20],
    [21, 22, 23, 19, 24]]
pprint.pprint(PUZZLE)
print(slide_puzzle(PUZZLE))
PUZZLE = [
    [17, 9, 6, 11, 5],
    [22, 13, 7, 18, 20],
    [8, 16, 2, 12, 15],
    [1, 24, 10, 3, 4],
    [21, 23, 19, 0, 14]]
pprint.pprint(PUZZLE)
print(slide_puzzle(PUZZLE))
PUZZLE = [
    [7, 18, 22, 2, 5],
    [12, 6, 3, 0, 9],
    [1, 8, 17, 4, 15],
    [19, 21, 14, 10, 20],
    [16, 23, 13, 11, 24]]
pprint.pprint(PUZZLE)
print(slide_puzzle(PUZZLE))
PUZZLE = [
    [7, 18, 22, 2, 5],
    [12, 6, 3, 0, 9],
    [1, 8, 17, 4, 15],
    [19, 21, 14, 10, 20],
    [16, 23, 13, 11, 24]]
pprint.pprint(PUZZLE)
print(slide_puzzle(PUZZLE))
PUZZLE = [
    [13, 1, 9, 14, 3, 12],
    [2, 7, 10, 15, 4, 18],
    [19, 21, 27, 17, 5, 6],
    [33, 31, 16, 8, 22, 24],
    [25, 0, 32, 35, 11, 34],
    [20, 28, 26, 30, 29, 23]]
pprint.pprint(PUZZLE)
print(slide_puzzle(PUZZLE))
