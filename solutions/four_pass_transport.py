"""

My solution for Four Pass Transport kata:
https://www.codewars.com/kata/four-pass-transport

Level: 1 kyu

Useful learning sources:
https://www.redblobgames.com/pathfinding/a-star/introduction.html
https://en.wikipedia.org/wiki/Travelling_salesman_problem
https://en.wikipedia.org/wiki/A*_search_algorithm
https://www.geeksforgeeks.org/a-search-algorithm/

"""

import itertools
import copy

CONV_BELT_MOD = 'c' # representation for one conveyer belt module
ATTENUATION = 0.001

def show(stations, path):
    """
    Helper function to display factory floor, stations and conveyer belt modules.
    """
    symbols = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}
    floor = [[None] * 10 for _ in range(0, 10)]
    for p in path:
        if p in stations:
            symbol = symbols[stations.index(p)]
        row, col = convert(p)
        floor[row][col] = symbol
    for i, s in enumerate(stations):
        row, col = convert(s)
        floor[row][col] = i + 1
    print('  0 1 2 3 4 5 6 7 8 9')
    for i, row in enumerate(floor):
        line = str(i) + ' ' + ' '.join([str(col) if col else '.'
                                        for col in row])
        print(line)

def convert(pos):
    """
    Convert single integer representation of position coordinates (e.g. 34) to
    two integer representation (e.g. row: 3, column: 4).
    """
    row = pos // 10
    col = pos % 10
    return row, col

class NoNeighbourError(Exception):
    """ Error to be raised when tile has no neighbours."""
    pass

class NoPathError(Exception):
    """ Error to be raised when issues with finding a path between stations."""
    pass

class TileOccupiedError(Exception):
    """ Error to be raised when a occupied tile is selected as path element."""
    pass

class Factory:
    """
    Represent the factory floor as an object.
    """

    def __init__(self, stations):
        self.floor = [[None] * 10 for _ in range(0, 10)]
        self.stations = {}
        self.occupied = set()
        self.place_stations(stations)
        self.empty_floor = copy.deepcopy(self.floor)
        self.empty_occupied = copy.deepcopy(self.occupied)

    def place_stations(self, stations):
        """
        Place the stations on the factory floor.
        """
        for i, station in enumerate(stations):
            station_num = i + 1
            row = station // 10
            col = station % 10
            self.floor[row][col] = station_num
            self.stations[station_num] = (row, col)
            self.mark_occupied([(row, col)])

    def place_conveyer_belt(self, row, col):
        """
        Place one conveyer belt module on the factory floor.
        """
        self.floor[row][col] = CONV_BELT_MOD
        self.mark_occupied([(row, col)])

    def remove_conveyer_belts(self):
        """ Remove all conveyer belts from factory floor. """
        self.floor = copy.deepcopy(self.empty_floor)
        self.occupied = copy.deepcopy(self.empty_occupied)

    def mark_occupied(self, tiles):
        """
        Mark tile occupied.
        """
        for row, col in tiles:
            self.occupied.add((row, col))

    def unmark_occupied(self, tiles):
        """
        Unmark tile occupied status.
        """
        for row, col in tiles:
            self.occupied.discard((row, col))

    def is_occupied(self, tile):
        """
        Return true if a tile of the factory floor is occupied either by a
        station or by a conveyer belt module.
        """
        row, col = tile
        return (row, col) in self.occupied

    def show_state(self):
        """
        Print a top view of the factory floor. Useful for troubleshooting.
        """
        print('  0 1 2 3 4 5 6 7 8 9')
        for i, row in enumerate(self.floor):
            line = str(i) + ' ' + ' '.join([str(col) if col else '.'
                                            for col in row])
            print(line)

class PathPlanner:
    """
    Plans the shortest path through the factory floor.
    """

    def __init__(self, factory):
        self.factory = factory
        self.occupied_tiles = list(self.factory.stations.values())
        self.min_path_segments = None
        self.min_path_order = None
        self.min_path_len = None

    def plan(self):
        """
        Main function. Uses A* algorithm with combinations of heuristics and 
        path segment orders to find shortest overall path that crosses a series
        of stations.

        A path segment is the path between two stations. With four stations 
        there are three segments: segment 1: station 1 - station 2, 
        segment 2: station 2 - station 3, segment 3: station 3 - station 4). A*
        finds the shortest path for individual segments. However, this does not
        guarantee overall shortest path. The overall path length is highly
        dependent on the order in which the segments are processed. The
        algorithm used in this solution runs A* for all permutations of the
        path segments.

        In addition to path segment permutations the algorithm varies the
        heuristics used by the A* search function. Tests showed that forcing A*
        to prefer straight horizontal or vertical paths seems to help finding
        optimum solutions However, this is no proof that this approach will
        always find the shortest overall path.
        """
        segment_variants = self.get_segment_variants()
        for segment_set in segment_variants:
            self.factory.remove_conveyer_belts()
            order, segments = self.get_order_segments(segment_set)
            try:
                path_segments = self.plan_stations_set(segments)
            except NoNeighbourError:
                continue
            except NoPathError:
                continue
            except TileOccupiedError:
                continue
            self.save_min_path(path_segments, order)
        min_path = self.join_paths()
        return min_path

    def get_segment_variants(self):
        """
        Generate a list of all segment orders + A* heuristics to be tested.
        
        First all permutations of segment orders are generated. Then, for each
        order each segment gets each heuristic assigned.
        
        For four stations and two heuristics this generates the following number
        of segment variants:
            - permutations of 3 segments = 6 variants in segment order
            - each segment tested with 2 heuristics = 2^3 = 8 heuristic variants 
              for one segment order
            - 6 segment orders * 8 heuristic variants = 48 segment variants to
              be tested
        """
        stations = list(self.factory.stations.values())
        ordered_segments = [(i, (stations[i], stations[i + 1]))
                            for i in range(len(stations) - 1)]
        segment_variants = list(itertools.permutations(ordered_segments, 3))
        heur_funcs = [
#                       'heur_no_heuristic',
#                       'heur_manhattan',
#                       'heur_manhattan_cross',
                    'heur_manhattan_vertical',
                    'heur_manhattan_horizontal'
                     ]
        heur_combs = list(itertools.product(heur_funcs, repeat=3))
        segment_variants = [((o1, (s1, h1)), (o2, (s2, h2)), (o3, (s3, h3)))
                            for ((o1, s1), (o2, s2), (o3, s3)) in segment_variants
                            for (h1, h2, h3) in heur_combs]
        return segment_variants

    def get_order_segments(self, segment_set):
        """
        Return the order of segments. This is required to recombine the
        individual path segments in the correct order to the total path.
        """
        order = [o for o, _ in segment_set]
        segments = [s for _, s in segment_set]
        return order, segments

    def plan_stations_set(self, segments):
        """
        Plan the shortest path between stations and place conveyer belt modules.
        """
        path_segments = []
        for (start_tile, end_tile), heuristic in segments:
            self.factory.unmark_occupied([start_tile, end_tile])
            path = self.get_Astar_path(start_tile, end_tile, heuristic)
            self.factory.mark_occupied([start_tile, end_tile])
            self.place_conveyer_modules(path)
            path_segments.append(path)
        return path_segments

    def save_min_path(self, path_segments, order):
        """
        Keep the shortest of two paths.
        """
        if not self.min_path_segments:
            self.min_path_segments = path_segments
            self.min_path_order = order
            self.min_path_len = sum(map(len, path_segments))
        else:
            lenght = sum(map(len, path_segments))
            if lenght < self.min_path_len:
                self.min_path_segments = path_segments
                self.min_path_order = order
                self.min_path_len = lenght

    def join_paths(self):
        """
        Join the path segments together to one list. Avoid duplicate
        elements when joining the segments.
        """
        if not self.min_path_order:
            return None
        stations = self.factory.stations
        path = []
        for i, _ in enumerate(self.min_path_order):
            seg = self.min_path_segments[self.min_path_order.index(i)]
            path = path + seg[:-1]
        path = path + [stations[len(stations)]] # add last station
        path = self.convert(path)
        return path

    def get_Astar_path(self, start_tile, end_tile, heuristic):
        graph = self.build_graph(start_tile, end_tile)
        path = self.astar(start_tile, end_tile, heuristic, graph)
        if not path:
            raise NoPathError('ERROR: no path from {} to {} found.'.format(start_tile, end_tile))
        return path

    def astar(self, start_tile, end_tile, heuristic, graph):
        heuristic_func = getattr(self, heuristic, self.heur_generic)
        closed_set = {}
        open_set = {start_tile: heuristic_func(start_tile, start_tile, end_tile)}
        came_from = {}
        g_score = {start_tile: 0}
        while open_set:
            current = min(open_set, key=open_set.get)
            if current == end_tile:
                return self.reconstruct_path(came_from, current)
            closed_set[current] = open_set[current]
            open_set.pop(current)
            neighbour_dists = graph[current]
            for neighbour in neighbour_dists:
                neighbour_g = g_score[current] + neighbour_dists[neighbour]
                neighbour_f = neighbour_g + \
                              heuristic_func(start_tile, neighbour, end_tile)
                if neighbour in open_set and \
                   neighbour_f > open_set[neighbour]:
                    continue
                if neighbour in closed_set and \
                   neighbour_f > closed_set[neighbour]:
                    continue
                elif neighbour in g_score and \
                   neighbour_g < g_score[neighbour]:
                    continue
                came_from[neighbour] = current
                g_score[neighbour] = neighbour_g
                open_set[neighbour] = neighbour_f
        return None
    
    def heur_generic(self, start, current, end):
        raise Exception('Unknown heuristic function')

    def heur_no_heuristic(self, start, current, end):
        h = 0
        return h

    def heur_manhattan(self, start, current, end):
        h = self.manhattan_dist(current, end)
        return h

    def heur_manhattan_cross(self, start, current, end):
        h = self.manhattan_dist(current, end) + \
            self.cross_product(start, current, end)
        return h

    def heur_manhattan_vertical(self, start, current, end):
        h = self.manhattan_dist(current, end) + \
            self.vertical_dist(current, end)
        return h
    
    def heur_manhattan_horizontal(self, start, current, end):
        h = self.manhattan_dist(current, end) + \
            self.horizontal_dist(current, end)
        return h        

    def manhattan_dist(self, start, end):
        s_row, s_col = start
        e_row, e_col = end
        dist = abs(e_row - s_row) + abs(e_col - s_col)
        return dist
    
    def cross_product(self, start, current, end):
        s_row, s_col = start
        c_row, c_col = current
        e_row, e_col = end
        dx1 = c_col - e_col
        dy1 = c_row - e_row
        dx2 = s_col - e_col
        dy2 = s_row - e_row
        cross = abs(dx1 * dy2 - dx2*dy1)
        return cross * ATTENUATION
    
    def vertical_dist(self, current, end):
        c_row, _ = current
        e_row, _ = end
        return abs(e_row - c_row) * ATTENUATION
    
    def horizontal_dist(self, current, end):
        ATTENUATION = 0.001
        _, c_col = current
        _, e_col = end
        return (e_col - c_col) * ATTENUATION

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()
        return path

    def place_conveyer_modules(self, path):
        """
        Place conveyer belt modules along the list of tiles provided.
        """
        for tile in path[1:-1]: # exclude start and end station tiles
            row, col = tile
            self.factory.place_conveyer_belt(row, col)

    def convert(self, path):
        """
        Convert tile coordinates from '(row, col)' to single integer notation.
        """
        path_converted = list(map(lambda tile: tile[0] * 10 + tile[1], path))
        return path_converted

    def build_graph(self, start_tile, end_tile):
        """
        Build a graph representation of the factory floor. The floor tiles are
        the nodes and distance between nodes is always 1. Tiles with conveyer
        belt modules are considered as occupied and will be excluded when
        building the graph. Stations except the start and end station are
        excluded as well. This way the algorithm calculates paths around
        occupied tiles.
        """
        floor_dim = len(self.factory.floor)
        tiles = set(itertools.product(range(0, floor_dim), repeat=2))
        tiles = tiles - self.factory.occupied
        distance = 1
        graph = {}
        for row, col in tiles:
            n_tiles = self.get_neighbour_tiles(row, col)
            if ((row, col) == start_tile or (row, col) == end_tile) and \
               not n_tiles:
                # start and/or end tile are isolated, they have no neighbours,
                # stop algorithm, not worth continuing
                raise NoNeighbourError('ERROR: tile {} has no neighbour tiles.'.format((row, col)))
            distances = {(n_row, n_col): distance for n_row, n_col in n_tiles \
                        if not self.factory.is_occupied((n_row, n_col))}
            graph[(row, col)] = distances
        return graph

    def get_neighbour_tiles(self, row, col):
        """
        Get all tiles around a given tile.
        """
        positions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        max_row = len(self.factory.floor) - 1
        max_col = len(self.factory.floor[0]) - 1
        neighbours = []
        for d_row, d_col in positions:
            n_row = row + d_row
            n_col = col + d_col
            if n_row >= 0 and n_row <= max_row and \
               n_col >= 0 and n_col <= max_col:
                neighbours.append((n_row, n_col))
        return neighbours

def four_pass(stations):
    """ main function """
    factory = Factory(stations)
    path_planner = PathPlanner(factory)
    path = path_planner.plan()
    return path
