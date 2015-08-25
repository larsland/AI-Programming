from heapq import heappush, heappop
from functools import wraps
from random import randrange
from pprint import pprint
from pandas import *
from math import sqrt, fabs
import itertools

counter = itertools.count()  # unique sequence count

class Node:
    # Constructor
    def __init__(self, x, y, tile):

        self.tile = tile
        # Reference to the board class
        # self.board = board

        # Coordinates
        self.x = x
        self.y = y

        # g and f scores
        self.g = 0
        self.h = lambda x,y: sqrt((x-self.x)**2 + (x-self.y)**2)
        self.f = 0

    def path(self):
        # Return a list of nodes forming the path from the root to this node.
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def update_priority(self, x, y):
        self.f = self.g + self.h(x, y) * 10  # A*

    def __lt__(self, other):  # comparison method for priority queue
        return self.f + self.g < other.f + other.g

    def __eq__(self, other):
        return isinstance(other, Node) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash("" + self.x + self.y)


class Board:
    def __init__(self):
        self.board_matrix = []  # Contains the entire board
        self.open = []  # List of open Nodes
        self.closed = []  # List of closed Nodes
        self.goal = None  # The goal Node
        self.start = None

        # Sizes defining the board
        self.width = 0
        self.height = 0

    # Calculate manhattan score for a given Node
    def manhattan_distance(self, node):
        return fabs(self.goal.x - node.x) + fabs(self.goal.y - node.y)

    def add_board(self, rows):
        x, y = 0, 0
        for row in rows:
            line = []
            x += 1
            for tile in row:
                y += 1
                if tile != '\n':
                    node = Node(self, x, y, tile)

                    if tile == 'B':
                        # Goal node is set
                        self.goal = node
                    elif tile == 'A':
                        # Start node is opened
                        self.start = node
                        heappush(self.open, node)
                    elif tile == '_':
                        # Normal nodes are added to open queue
                        heappush(self.open, node)
                    elif tile == '#':
                        # Walls are closed
                        heappush(self.closed, node)

                    line.append(node)
            self.board_matrix.append(line)

        self.width = x - 1
        self.height = y - 1

        print self.width, self.height

        # Define variables for the start Node
        if len(self.open) > 0:
            self.open[0].g = 0
            self.open[0].h = self.manhattan_distance(self.open[0])
            self.open[0].solution = True


    # Returns all parents for the current Node
    def get_parents(self, node):
        # Init array for the parents
        parents = []

        # Get valid parents that are in the map
        if node.y > 0:  # Up
            parents.append(self.board_matrix[node.y - 1][node.x])
        if node.y < self.height:  # Down
            parents.append(self.board_matrix[node.y + 1][node.x])
        if node.x > 0:  # Left
            parents.append(self.board_matrix[node.y][node.x - 1])
        if node.x < self.width:  # Right
            parents.append(self.board_matrix[node.y][node.x + 1])

        # Return list of parents
        return parents

    # Recursive reconstruct the path from goal to start
    def reconstruct_path(self, current):
        if current.navigated_from is not None:
            current.on_path = True
            self.reconstruct_path(current.navigated_from)


inf = float('inf')


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


def a_star(graph, s, t, h):
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


if __name__ == '__main__':
    n = 10

    G = """
    ....................
    ....................
    .........######.....
    ...........A..#..B..
    .........######.....
    ....................
    ...................."""

    b = Board()
    b.add_board(G)
    print b.board_matrix

    print "-------------------------------"
    print G
    print ""
    print "-------------------------------"

    # pprint(a_star(graph=G, s=G[0][1], t=G[n - 1][n - 2], h=lambda v: 0))

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

