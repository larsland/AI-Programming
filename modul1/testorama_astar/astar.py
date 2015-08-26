from heapq import heappush, heappop
from functools import wraps
from random import randrange
from pprint import pprint
from math import sqrt, fabs
from itertools import count


class Node:
    # Constructor
    def __init__(self, x, y, tile, board):
        # Coordinates
        self.x = x
        self.y = y

        self.tile = tile
        # Reference to the board class
        self.board = board

        # g and f scores
        self.g = 0
        self.h = lambda x, y: sqrt((self.x-x)**2 + (self.y-y)**2)
        # self.h = lambda x, y: fabs(x-self.x) + fabs(y-self.y)
        self.f = 0

        # Priority Queue counter in case equal priority
        self.c = 0

        self.siblings = []

    def path(self):
        # Return a list of nodes forming the path from the root to this node.
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # Generates the valid siblings for the Node within the board matrix
    def get_siblings(self):
        # Init array for the parents
        siblings = []

        b_matrix = self.board.board_matrix
        height = len(b_matrix)-1
        width = len(b_matrix[0])-1

        try:
            # Remember that when using x and y as indexes, you must calculate with -1.
            if self.y > 0:
                # Up
                # print("UP", b_matrix[self.y-1][self.x])
                siblings.append(b_matrix[self.y-1][self.x])
            if self.y < height:
                # Down
                # print("DOWN", b_matrix[self.y+1][self.x])
                siblings.append(b_matrix[self.y+1][self.x])
            if self.x > 0:
                # Left
                # print("LEFT", b_matrix[self.y][self.x-1])
                siblings.append(b_matrix[self.y][self.x-1])
            if self.x < width:
                # Right
                # print("RIGHT", b_matrix[self.y][self.x+1])
                siblings.append(b_matrix[self.y][self.x+1])
        except IndexError as e:
            print(e)
            print(self)
            print(height)

        # Return list of siblings
        return siblings

    def update_priority(self, goal, c):
        self.c = c
        self.f = self.g + self.h(goal.x, goal.y) * 10  # A*

    def __lt__(self, other):  # comparison method for priority queue
        return self.f + self.c < other.f + self.c

    def __repr__(self):
        return "<Node (x:%s, y:%s, f:%s, c:%s)>" % (self.x, self.y, self.f, self.c)

    # May not need these
    def __eq__(self, other):
        return isinstance(other, Node) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash("" + self.x + self.y)


class Board:
    def __init__(self, board):
        self.board = board  # Holds the input board for reference

        self.board_matrix = []  # Matrix of board Nodes
        self.open = []  # List of open Nodes
        self.closed = []  # List of closed Nodes
        self.solution_path = []  # List of nodes that make up the solution path
        self.goal = None  # The goal Node
        self.initial = None  # The initial Node

        self.counter = count()  # Unique sequence count for correct priority queue implementation

        # Sizes defining the board
        self.width = 0
        self.height = 0

        self.generate_matrix()

    def __repr__(self):
        representation = '<Board ([\n'
        for line in self.board[:-2]:
            representation += line+'\n'
        representation += self.board[-1] + '\n], \n'

        representation += 'initial node:  ' + str(self.initial) + '\n'
        representation += 'goal node:     ' + str(self.goal) + '\n)'
        representation += 'open:          ' + str(self.open) + '\n'
        representation += 'closed:        ' + str(self.closed) + '\n'
        representation += 'counter:       ' + str(next(self.counter)) + '\n'
        representation += 'solution path: ' + str(self.solution_path) + '\n'

        return representation

    def generate_matrix(self):
        self.height = len(self.board)-1
        self.width = max(map(len, self.board))-1

        y = -1
        for row in self.board:
            node_row = []
            y += 1
            x = -1
            for tile in row:
                x += 1
                if tile != '\n':
                    node = Node(x, y, tile, self)

                    if tile == 'B':
                        # Goal node is set
                        self.goal = node
                    elif tile == 'A':
                        # Start node is opened
                        self.initial = node
                        heappush(self.open, node)
                    elif tile == '_':
                        # Normal nodes are added to open queue
                        heappush(self.open, node)
                    elif tile == '#':
                        # Walls are closed
                        self.closed.append(node)

                    node_row.append(node)
            self.board_matrix.append(node_row)

    def a_star(self):
        path = []
        while self.open:
            node = heappop(self.open)
            if node in self.closed:
                continue
            path.append(node)
            self.closed.append(node)
            if node == self.goal:
                return path, len(path), True

            for sibling in node.get_siblings():
                if sibling in self.closed:
                    continue
                sibling.update_priority(self.goal, next(self.counter))
                heappush(self.open, sibling)

        return path, len(path), False

    def breadth_first_search(self):
        path = []
        while self.open:
            node = self.open.pop(0)
            if node in self.closed:
                continue
            path.append(node)
            self.closed.append(node)
            if node == self.goal:
                return path, len(path), True

            for sibling in node.get_siblings():
                self.open.append(sibling)
        return path, len(path), False

    def depth_first_search(self):
        path = []
        while self.open:
            node = self.open.pop()
            if node in self.closed:
                continue
            path.append(node)
            self.closed.append(node)
            if node == self.goal:
                return path, len(path), True

            for sibling in node.get_siblings():
                self.open.insert(0, sibling)

        return path, len(path), False

    def add_path(self, path, node, i):
        path_line = list(path[node.y])
        path_line[node.x] = 'x'
        path[node.y] = "".join(path_line)

        # print('-'*self.width + '-\n')
        # for line in path:
        #    print(str(line))

        return path

    def solve(self):
        path = self.board

        i = 0
        a_star_path, steps, found = self.a_star()
        # print(a_star_path, steps, found)
        if found:
            # print("Solution found in %s steps" % steps)
            for node in a_star_path:
                i += 1
                path = self.add_path(path, node, i)
        else:
            # print("No solution found in %s steps" % steps)
            for node in a_star_path:
                i += 1
                path = self.add_path(path, node, i)
        return path


class Astar:
    def __init__(self, problem):
        self.problem = problem
        self.open = []  # List of open Nodes
        self.closed = []  # List of closed Nodes
        self.goal = None  # The goal Node
        self.start = None  # The start Node

    def best_first_search(self):
        path = []
        while self.open:
            node = heappop(self.open)
            if node in self.closed:
                continue
            path.append(node)
            self.closed.append(node)
            if node == self.goal:
                return path, len(path), True

            for sibling in node.get_siblings():
                if sibling not in self.closed:
                    sibling.update_priority(self.goal, next(self.counter))
                    heappush(self.open, sibling)

        return path, len(path), False

    def breadth_first_search(self):
        path = []
        while self.open:
            node = self.open.pop()
            if node in self.closed:
                continue
            path.append(node)
            self.closed.append(node)
            if node == self.goal:
                return path, len(path), True

            for sibling in node.get_siblings():
                self.open.append(sibling)
        return path, len(path), False

    def depth_first_search(self):
        path = []
        for node in self.open:
            if node in self.closed:
                continue
            path.append(node)
            self.closed.append(node)
            if node == self.goal:
                return path, len(path), True

            for sibling in node.get_siblings():
                self.open.insert(0, sibling)

        return path, len(path), False

    def add_path(self, path, node, i):
        path_line = list(path[node.y])
        path_line[node.x] = 'x'
        path[node.y] = "".join(path_line)

        print('-'*self.problem.width + '-\n')
        for line in path:
            print(str(line))

        return path

    def solve(self, search):
        path = self.problem.input_rows

        i = 0
        node_path, steps, found = search()
        if found:
            print("Solution found in %s steps" % steps)
            for node in node_path:
                i += 1
                path = self.add_path(path, node, i)
        else:
            print("No solution found in %s steps" % steps)
            for node in node_path:
                i += 1
                path = self.add_path(path, node, i)
        return path





if __name__ == '__main__':
    G = [
    '..............#.....',
    '..............#.....',
    '.........######.....',
    '...........A..#..B..',
    '.........######.....',
    '..............#.....',
    '....................']


    for i in range(1000):
        b = Board(list(G))
        b.solve()
    #astar = Astar(b)
    #astar.solve(astar.best_first_search)

"""
class GraphProblem(Problem):
    # The problem of searching a graph from one node to another.
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph
        self.inf = float('inf')

    def actions(self, A):
        # The actions at a graph node are just its neighbors.
        return self.graph.get(A).keys()

    def result(self, state, action):
        # The result of going to a neighbor is just that neighbor.
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or self.inf)

    def h(self, node):
        # h function is straight-line distance from a node's state to goal.
        locs = getattr(self.graph, 'locations', None)
        if locs:
            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return self.inf


def astar_search(problem, h=None):
    # A* search is best-first graph search with f(n) = g(n)+h(n).
    # You need to specify the h function when you call astar_search, or
    # else in your Problem subclass.
    # h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


map1 =
    [['A', _]]

"""


def memo(func):
    cache = {}

    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrap

def heurestic(u, v):
    @memo
    def h(u, v):
        return u + v

    return h(u, v)


def a_star(self, graph, s, t, h):
    inf = float('inf')
    P, Q = {}, [(h(s), None, s)]
    while Q:
        d, p, u = heappop(Q)
        if u in P:
            continue
        P[u] = p
        if u == t:
            return d - h(t), P
        for v in graph[u]:
            w = graph[u][v] - h(u) + h(v)
            heappush(Q, (d + w, u, v))
    return inf, None