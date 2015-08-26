from heapq import heappush, heappop
from functools import wraps
from random import randrange
from pprint import pprint
from math import sqrt, fabs
import itertools

counter = itertools.count()  # unique sequence count


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
            print e
            print self
            print height

        # Return list of siblings
        return siblings

    def update_priority(self, goal):
        self.f = self.g + self.h(goal.x, goal.y) * 10  # A*

    def __lt__(self, other):  # comparison method for priority queue
        return self.f < other.f

    def __repr__(self):
        return "<Node (%s, %s, %s)>" % (self.x, self.y, self.f)

    # May not need these
    def __eq__(self, other):
        return isinstance(other, Node) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash("" + self.x + self.y)


class Board:
    def __init__(self):
        self.input_rows = [] # Contains the input to add board
        self.board_matrix = []  # Contains the entire board
        self.open = []  # List of open Nodes
        self.closed = []  # List of closed Nodes
        self.goal = None  # The goal Node
        self.start = None

        # Sizes defining the board
        self.width = 0
        self.height = 0

    # Calculate manhattan score for a given Node
    # def manhattan_distance(self, node):
    #    return fabs(self.goal.x - node.x) + fabs(self.goal.y - node.y)

    def add_board(self, rows):
        self.input_rows = rows
        self.width = len(rows)-1
        self.height = len(rows[0])-1

        y = -1
        for row in rows:
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
                        self.start = node
                        heappush(self.open, node)
                    elif tile == '_':
                        # Normal nodes are added to open queue
                        heappush(self.open, node)
                    elif tile == '#':
                        # Walls are closed
                        heappush(self.closed, node)

                    node_row.append(node)
            self.board_matrix.append(node_row)

    def run(self):
        path = []
        while self.open:
            node = heappop(self.open)
            path.append(node)
            for sibling in node.get_siblings():
                if sibling == self.goal:
                    print "Goal found!"
                    print 'PATH:', path
                    return path
                if sibling not in self.closed:
                    sibling.update_priority(self.goal)
                    heappush(self.open, sibling)

            heappush(self.closed, node)



        #print self.open
        #print self.closed

    def add_path(self, path, node, i):
        print node
        path_line = list(path[node.y])
        # path_line = '......1..#...B..'
        path_line[node.x] = 'x'
        #print 'path_line', path_line
        # '......A..#...B..' = '......1..#...B..'
        path[node.y] = "".join(path_line)

        for line in path:
            print str(line)


        return path

    def write_solution(self):
        path = self.input_rows

        i = 0
        for node in self.run():
            i += 1
            path = self.add_path(path, node, i)

        #for line in path:
        #    print line


    # Recursive reconstruct the path from goal to start
    def reconstruct_path(self, current):
        if current.navigated_from is not None:
            current.on_path = True
            self.reconstruct_path(current.navigated_from)


inf = float('inf')


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

    G = [
    '....................',
    '....................',
    '.........######.....',
    '...........A..#..B..',
    '.........######.....',
    '....................',
    '....................']

    # b = Board()
    # b.add_board(G)
    # print(b.board_matrix)
    # print(len(b.board_matrix), b.width)
    # print(len(b.board_matrix[0]), b.height)


    b = Board()
    b.add_board(open('boards/board-1-1.txt').readlines())
    b.write_solution()
    # print(b.board_matrix)

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


