"""

My solution for The Lift kata:
https://www.codewars.com/kata/the-lift

Level: 3 kyu

"""

UP = 1
DOWN = -1

class Dinglemouse(object):
    """ The Lift solver class """

    def __init__(self, queues, capacity):
        self.queues = tuples_to_list(queues)
        self.top_floor = len(self.queues) - 1
        self.ground_floor = 0
        self.capacity = capacity
        self.passengers = []
        self.stops = [0]
        self.floor = 0
        self.direction = UP

    def theLift(self):
        """ main function """
        while not self.floor_queues_empty() or not self.lift_is_empty():
            if self.stop_lift():
                self.passengers_leaving()
                self.passengers_entering()
            if self.floor == self.top_floor:
                self.direction = DOWN
            if self.floor == self.ground_floor:
                self.direction = UP
            self.floor += self.direction
        if self.stops[-1:] != [0]:
            self.stops.append(0)
        return self.stops

    def floor_queues_empty(self):
        """ check if floor queues are empty """
        return is_list_empty(self.queues)

    def lift_is_empty(self):
        """ check if lift is empty """
        return False if self.passengers else True

    def stop_lift(self):
        """ check whether the lift needs to stop """
        to_enter = [p for p in self.queues[self.floor]
                    if (self.direction == UP and p > self.floor) or \
                       (self.direction == DOWN and p < self.floor)]
        if self.floor in self.passengers or to_enter:
            self.stops.append(self.floor)
            return True
        return False

    def passengers_leaving(self):
        """ passengers leaving the lift """
        remain = [p for p in self.passengers if p != self.floor]
        if len(remain) != len(self.passengers):
            self.passengers = remain

    def passengers_entering(self):
        """ passengers enter the lift """
        passengers = self.queues[self.floor][:]
        for passenger in passengers:
            if len(self.passengers) < self.capacity and \
               ((self.direction == UP and passenger > self.floor) or \
                (self.direction == DOWN and passenger < self.floor)):
                self.passengers.append(passenger)
                self.queues[self.floor].pop(self.queues[self.floor].index(passenger))

def tuples_to_list(i):
    """ transform nested tuples to nested lists """
    if isinstance(i, (tuple, list)):
        l = [list(e) if isinstance(e, tuple) else e for e in i]
    else:
        return i
    for i, e in enumerate(l):
        l[i] = tuples_to_list(e)
    return l

def is_list_empty(in_list):
    """ check if all elements of a nested list are empty """
    if isinstance(in_list, list):
        return all(map(is_list_empty, in_list))
    return False

if __name__ == "__main__":
    q = ((), (0,), (), (), (2,), (3,), ())
    lift = Dinglemouse(q, 5)
    lift_stops = lift.theLift()
    print(lift_stops)
