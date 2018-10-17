"""

My solution for The Lift kata:
https://www.codewars.com/kata/the-lift

Level: 3 kyu

"""

class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.queues = queues
        self.capacity = capacity
        
    def theLift(self):
        stops = []
        direction = 1
        floor = 0
        while not is_tuple_empty(self.queues):
            if self.queues[floor]:
                pass
        return stops

def is_tuple_empty(in_tuple):
    if isinstance(in_tuple, tuple):
        return all(map(is_tuple_empty, in_tuple))
    return False


if __name__ == "__main__":
    q = ((), (0,), (), (), (2,), (3,), ())
    lift = Dinglemouse(q, 5)
    lift_stops = lift.theLift()
