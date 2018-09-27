"""

My solution for Four Pass Transport kata:
https://www.codewars.com/kata/four-pass-transport

Level: 1 kyu

https://en.wikipedia.org/wiki/Travelling_salesman_problem

"""

import itertools
import copy

CONV_BELT_MOD = 'c' # representation for one conveyer belt module

def show(stations, path):
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
    row = pos // 10
    col = pos % 10
    return row, col

class NoNeighbourError(Exception):
    """ Error to be raised when tile has no neighbours."""
    pass

class NoPathError(Exception):
    """ Error to be raised when issues with finding a path between stations."""
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
        """ remove all conveyer belts from factory floor """
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

    def is_occupied(self, row, col):
        """
        Return true if a tile of the factory floor is occupied either by a
        station or by a conveyer belt module.
        """
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

    def plan(self):
        """
        Main function. Uses Djikstra algorithm to find shortest path between
        stations. Djikstra does not guarantee to find the total shortest path
        between all stations. Total path length depends on the order in which
        which path segments are determined.

        To find shortest total path length plan runs through all permutations
        of segment combinations and returns min_path or None if not path could
        be found.
        """
        segment_variants = self.get_segment_variants()
        min_path = None
        for segment_set in segment_variants:
            self.factory.remove_conveyer_belts()
            order, segments = self.get_order_segments(segment_set)
            try:
                path_segments = self.plan_stations_set(segments)
            except NoNeighbourError:
                continue
            except NoPathError:
                continue
            path = self.join_paths(path_segments, order)
            min_path = self.get_min_path(path, min_path)
        return min_path
    
    def planv2(self):
        S1 = ('S1_1', 'S1_2', 'S1_3', 'S1_4')
        S2 = ('S2_1', 'S2_2', 'S2_3', 'S2_4')
        S3 = ('S3_1', 'S3_2', 'S3_3', 'S3_4')
        S4 = ('S4_1', 'S4_2', 'S4_3', 'S4_4')
        seg1_2 = list(zip(itertools.repeat(0), itertools.product(S1, S2)))
        seg2_3 = list(zip(itertools.repeat(1), itertools.product(S2, S3)))
        seg3_4 = list(zip(itertools.repeat(2), itertools.product(S3, S4)))
        segment_variants = []
        for seg_comb in itertools.product(seg1_2, seg2_3, seg3_4):
            segment_variants = segment_variants + list(itertools.permutations(seg_comb, 3))

    def get_segment_variants(self):
        """ Generate list of all permutations of the segment order. """
        stations = list(self.factory.stations.keys())
        ordered_segments = [(i, (station, station + 1))
                            for i, station in enumerate(stations[:-1])]
        segment_variants = list(itertools.permutations(ordered_segments, 3))
        return segment_variants

    def get_order_segments(self, segment_set):
        """
        Return the order of segments. This is required to recombine the
        individual path segments in the correct order to the total path.
        """
        order = [o for o, _ in segment_set]
        segments = [s for _, s in segment_set]
        return order, segments

    def get_min_path(self, path, min_path):
        """
        Keep the shortest of two paths.
        """
        if not min_path:
            min_path = path
        else:
            min_path = path if len(path) < len(min_path) else min_path
        return min_path

    def join_paths(self, path_segments, order):
        """
        Join the path segments together to one list. Avoid duplicate
        elements when joining the segments.
        """
        path = []
        for i, _ in enumerate(order):
            seg = path_segments[order.index(i)]
            if path and path[-1] == seg[0]:
                path = path + seg[1:] # skip first element to avoid duplicates
            else:
                path = path + seg
        return path

    def plan_stations_set(self, stations):
        """
        Plan the shortest path between stations and place conveyer belt modules.
        """
        path_segments = []
        for start_station, end_station in stations:
            start_tile = self.factory.stations[start_station]
            end_tile = self.factory.stations[end_station]
            path = self.get_shortest_path(start_tile, end_tile)
            self.place_conveyer_modules(path[1:-1])
            path_segments.append(self.convert(path))
        return path_segments

    def place_conveyer_modules(self, path):
        """
        Place conveyer belt modules along the list of tiles provided.
        """
        for tile in path: # exclude start station when placing conv. modules
            row, col = tile
            self.factory.place_conveyer_belt(row, col)

    def convert(self, path):
        """
        Convert tile coordinates from '(row, col)' to single digit notation.
        """
        path_converted = list(map(lambda tile: tile[0] * 10 + tile[1], path))
        return path_converted

    def get_shortest_path(self, start_tile, end_tile):
        """
        Calculate a sequence of tiles to be moved that get a tile to the target
        position. Uses Dijkstra algorithm for shortest path calculation.
        """
        graph = self.build_graph(start_tile, end_tile)
        distances = self.calculate_distances(start_tile, graph)
        tile_sequence = self.get_shortest_sequence(distances, graph,
                                                   start_tile,
                                                   end_tile)
        tile_sequence.reverse()
        return tile_sequence

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
        self.factory.unmark_occupied([start_tile, end_tile])
        tiles = set(itertools.product(range(0, floor_dim), repeat=2))
        tiles = tiles - self.factory.occupied
        distance = 1
        graph = {}
        for row, col in tiles:
            n_tiles = self.get_neighbour_tiles(row, col)
            distances = {(n_row, n_col): distance for n_row, n_col in n_tiles \
                        if not self.factory.is_occupied(n_row, n_col)}
            graph[(row, col)] = distances
        self.factory.mark_occupied([start_tile, end_tile])
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

    def calculate_distances(self, start_tile, graph):
        """
        Perform the distance calculations required for the Dijkstra algorithm.

        Based on this introduction to the Dijkstra algorithm:
        https://brilliant.org/wiki/dijkstras-short-path-finder/
        """
        infinity = float('inf')
        unvisited = [vertex for vertex in graph]
        distances = {vertex: infinity for vertex in unvisited}
        distances[start_tile] = 0
        # calculate distances from source
        while unvisited:
            unvisited_dist = {v:distances[v] for v in unvisited}
            vertex = min(unvisited_dist, key=unvisited_dist.get)
            unvisited.remove(vertex)
            if not graph[vertex] and vertex == start_tile:
                raise NoNeighbourError('ERROR: tile {} has no neighbour tiles.'.format(vertex))
            for neighbor in graph[vertex]:
                alt = distances[vertex] + graph[vertex][neighbor]
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
        return distances

    def get_shortest_sequence(self, distances, graph, start_tile, end_tile):
        """
        After the graph has been build and the distances within the graph
        have been calculated, this function works out the shortest sequence of
        tiles.
        """
        if not graph[end_tile]:
            raise NoPathError('ERROR: no path to tile {} found.'.format(end_tile))
        tile = end_tile
        tile_sequence = []
        while not tile == start_tile:
            neighbour_dist = {neighbour:distances[neighbour] for neighbour in graph[tile]}
            if self.all_dist_infinite(neighbour_dist):
                raise NoPathError('ERROR: no path to tile {} found.'.format(tile))
            tile_sequence.append(tile)
            tile = min(neighbour_dist, key=neighbour_dist.get)
        tile_sequence.append(start_tile)
        return tile_sequence

    def all_dist_infinite(self, neighbor_dist):
        """
        Check if distances to all neighbour tiles are infinite. This is the case
        when no path between stations could be found (e.g. factory floor
        separated by conveyer belt.)
        """
        dists = set(neighbor_dist.values())
        return len(dists) == 1 and float('inf') in dists

def four_pass(stations):
    """ main function """
    factory = Factory(stations)
    path_planner = PathPlanner(factory)
    path = path_planner.plan()
    return path

print('\nshortest path:\n')
show([62, 67, 36, 86],
     [62, 63, 64, 65, 66, 67, 57, 56, 46, 36, 37, 38, 48, 58, 68, 78, 88,
      87, 86])
print('\nmy solution:\n')
show([62, 67, 36, 86],
     [62, 63, 64, 65, 66, 67, 57, 47, 37, 36, 26, 27, 28, 38, 48, 58, 68, 78,
      77, 76, 86])

print('\nshortest path:\n')
show([83, 79, 96, 7],
     [83, 73, 74, 75, 76, 77, 78, 79, 89, 88, 87, 86, 96, 95, 94, 93, 92, 82,
      72, 62, 52, 42, 32, 22, 12, 2, 3, 4, 5, 6, 7])
print('\nmy solution:\n')
show([83, 79, 96, 7],
     [83, 84, 74, 64, 65, 66, 67, 68, 69, 79, 78, 77, 76, 86, 96, 95, 94, 93,
      92, 82, 72, 73, 63, 53, 54, 44, 34, 24, 25, 26, 16, 6, 7])

print('\nshortest path:\n')
show([3, 7, 22, 6],
     [3, 2, 1, 11, 21, 31, 32, 33, 34, 35, 36, 37, 38, 28, 18, 8, 7, 17, 27,
      26, 25, 24, 23, 22, 12, 13, 14, 15, 16, 6])
print('\nmy solution:\n')
show([3, 7, 22, 6],
     [3, 2, 1, 11, 21, 31, 41, 42, 43, 44, 45, 46, 47, 48, 38, 28, 18, 8, 7,
      17, 27, 37, 36, 35, 34, 33, 32, 22, 23, 24, 25, 26, 16, 6])
