"""

My solution for Four Pass Transport kata:
https://www.codewars.com/kata/four-pass-transport

Level: 1 kyu

"""

import itertools

CONV_BELT_MOD = 9 # a numerical representation of one conveyer belt module

class FactoryFloor:
    """
    Represent the factory floor as an object.
    """

    def __init__(self, stations):
        self.floor = [[None] * 10 for _ in range(0, 10)]
        self.stations = {}
        self.place_stations(stations)

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

    def place_conveyer_belt(self, row, col):
        """
        Place one conveyer belt module on the factory floor.
        """
        self.floor[row][col] = CONV_BELT_MOD

    def show_floor(self):
        """
        Print a top view of the factory floor. Useful for troubleshooting.
        """
        print('  0 1 2 3 4 5 6 7 8 9')
        for i, row in enumerate(self.floor):
            line = str(i) + ' ' + ' '.join([str(col) if col else '.'
                                            for col in row])
            print(line)

class PathPlanner:
    
    def __init__(self, factory_floor):
        self.factory_floor = factory_floor
        self.occupied_tiles = list(self.factory_floor.stations.values())

    def get_shortest_path(self, start_tile, target_row, target_col):
        """
        Calculate a sequence of tiles to be moved that get a tile to the target
        position. Uses Dijkstra algorithm for shortest path calculation.
        """
        graph = self.build_graph(start_tile, end_tile)
        distances = self.calculate_distances(start_tile, graph)
        tile_sequence = self.get_shortest_tile_sequence(distances, graph,
                                                        start_tile,
                                                        target_row, target_col)
        tile_sequence.reverse()
        return tile_sequence

    def build_graph(self, start_tile, end_tile):
        """
        Build a graph representation of the factory floor. The floor tiles are 
        the nodes and distance between nodes is always 1. Tiles with conveyer 
        belt modules are considered as occupied and will be excluded when 
        building the graph. Stations except the target station are excluded as 
        well. This way the algorithm calculates paths around occupied tiles.
        """
        floor_dim = len(self.factory_floor.floor)
        self.unmark_occupied([start_tile, end_tile])
        distance = 1
        graph = {}
        for row, col in itertools.product(range(0,floor_dim), repeat=2):
            surrounding_tiles = self.get_surrounding_tiles(row, col)
            for n_row, n_col in surrounding_tiles:
                if not self.factory_floor.floor[n_row][n_col] == CONV_BELT_MOD and \
                not 
        

        return graph

    def get_surrounding_tiles(self, row, col):
        """
        Get all tiles around a given tile.
        """
        positions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        max_row = len(self.factory_floor.factory_floor) - 1
        max_col = len(self.factory_floor.factory_floor[0]) - 1
        neighbours = []
        for d_row, d_col in positions:
            n_row = row + d_row
            n_col = col + d_col
            if n_row >= 0 and n_row <= max_row and \
               n_col >= 0 and n_col <= max_col:
                neighbours.append((n_row, n_col))
        return neighbours






        t_row, t_col = self.get_position(tile)
        sequence = []
        for d_row, d_col in positions:
            n_row = t_row + d_row
            check_col = t_col + d_col
            if n_row >= 0 and n_row <= self.puzzle_size - 1 and \
               check_col >= 0 and check_col <= self.puzzle_size - 1:
                sequence.append(self.tile_array[n_row][check_col])
            else:
                sequence.append(None)
        return sequence

    def calculate_distances(self, start_tile, graph):
        """
        Perform the distance calculations required for the Dijkstra algorithm.
        """
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
        """
        After the graph has been build and the distances within the graph
        have been calculated, this function works out the sequence of tiles
        to be moved.
        """
        tile = self.tile_array[target_row][target_col]
        tile_sequence = []
        while not tile == start_tile:
            neighbor_dist = {neighbor:distances[neighbor] for neighbor in graph[tile]}
            tile_sequence.append(tile)
            tile = min(neighbor_dist, key=neighbor_dist.get)
        return tile_sequence





def four_pass(stations):
    """ main function """
    factory_floor = FactoryFloor(stations)
    factory_floor.show_floor()
    path_planner = PathPlanner(factory_floor)
    

four_pass([1, 69, 95, 70])
