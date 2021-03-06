import config
import itertools
import sys
import time

def get_mins(L, scorer):
    minimum = min(map(scorer, L))
    return [item for item in L if scorer(item) == minimum]

CANNOT_MOVE = False
class Generator:
    def __init__(self, knight):
        self.knight = knight
        knight.location.visited = True

    def run(self, out):
        for visited in itertools.count(1):
            self.knight.write_current_data(out)
            out.write("\n")
            if (self.knight.move() == CANNOT_MOVE):
                break
        return visited

class Knight:
    def __init__(self, location, initial_rule):
        (self.location, self.rule, self.tiebreak) = (location, initial_rule, False)

    def write_current_data(self, out):
        out.write("{'square':%s, 'tiebreak':%s}" % (str(self.location), self.tiebreak))

    def move(self):
        if (self.location.has_no_neighbours()):
            return False
        self.rule = self.rule.transition(self.location)
        (self.location, self.tiebreak) = self.rule.apply_to(self.location)
        self.location.visited = True
        return True

class Rule:
    def __init__(self, ordering, switch_square, next_rule):
        (self.ordering, self.switch_square, self.next_rule) = (ordering, switch_square, next_rule)

    def transition(self, square):
        return self.next_rule if (square.equals(self.switch_square)) else self
    
    def apply_to(self, square):
        return square.pick_neighbour(lambda x : x["square"].degree(), \
                                     lambda x : self.ordering.find(str(x["direction"])))

class Square:
    def __init__(self, board, x, y):
        (self.board, self.x, self.y) = (board, x, y)
        self.visited = False

    def equals(self, square):
        return (self.x == square.x and self.y == square.y) if square else False

    def __str__(self):
        return "(%d,%d)" % (self.x, self.y)

    def degree(self):
        return len(self.board.get_unvisited_neighbours(self))

    def has_no_neighbours(self):
        return (0 == self.degree())

    def pick_neighbour(self, scorer, tiebreaker):
        candidates = get_mins(self.board.get_unvisited_neighbours(self), scorer)
        return [candidates[0]["square"], False] if 1 == len(candidates) \
          else [get_mins(candidates, tiebreaker)[0]["square"], True]

class Board:
    def __init__(self, dim):
        self.dim = dim
        self.squares = [[Square(self, x, y) for y in range(1, dim+1)] for x in range(1, dim+1)]
        self.directions = [Direction(number=1, x=-2, y=1 ), \
                           Direction(number=2, x=-1, y=2 ), \
                           Direction(number=3, x=1,  y=2 ), \
                           Direction(number=4, x=2,  y=1 ), \
                           Direction(number=5, x=2,  y=-1), \
                           Direction(number=6, x=1,  y=-2), \
                           Direction(number=7, x=-1, y=-2), \
                           Direction(number=8, x=-2, y=-1)]
        self.neighbours = dict([(s, self.compute_neighbours(s)) for r in self.squares for s in r])

    def get_square_at(self, x, y):
        return self.squares[x-1][y-1] if (x in range(1, self.dim+1) and y in range(1, self.dim+1)) else None

    def get_unvisited_neighbours(self, square):
        return filter(lambda x : not x["square"].visited, self.neighbours[square])

    def compute_neighbours(self, square):
	return [{"direction":d.number, "square":d.apply(square)} for d in self.directions if d.apply(square)]

class Direction:
    def __init__(self, number, x, y):
        (self.number, self.x, self.y) = (number, x, y)

    def apply(self, square):
        return square.board.get_square_at(x = square.x + self.x, y = square.y + self.y)

def run(dim, out):
    out.write("%d\n" % (dim,))
    board = Board(dim)
    rules = config.get_rules(m = dim, board = board)
    knight = Knight(location = board.get_square_at(x = 1, y = 1), initial_rule = rules[0])
    generator = Generator(knight)
    return generator.run(out)

def now():
    return int(time.time())

if __name__ == '__main__':
    n = int(sys.argv[1])
    sys.stderr.write("Generating tour for dimension %d\n" % (n,))
    start = now()
    visited = run(dim = int(sys.argv[1]), out = sys.stdout)
    finish = now()
    if (visited == n*n):
        sys.stderr.write("SUCCESS - generated tour for dimension %d in %d seconds\n" %(n, finish-start))
    else:
        sys.stderr.write("FAILED - Only visited %d of %d squares in %d seconds\n" %(visited, n*n, finish-start))

