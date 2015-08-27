from heapq import heappush, heappop
from functools import wraps
from random import randrange
from pprint import pprint
from math import sqrt, fabs
from itertools import count


class Node:
    def __init__(self, state, problem, parent=None, action=None, path_cost=0):
        self.state = state
        self.problem = problem
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash("" + self.state)


class Problem():
    def __init__(self, state, initial, goal=None, ):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.state = state
        self.initial = initial
        self.goal = goal

    def init_state(self):
        """Initialization method for the state of the problem,
        can be a list, matrix, tree or any other data structure that fits the problem"""
        pass

    def actions(self, state):
        """Returns all actions that can be performed from current state,
        either as a data structure or a generator"""
        pass

    def solve(self, algorithm):
        """Solve the problem with the given algorithm"""
        pass

    def goal_test(self, other):
        return self.goal == other

    def save_state(self):
        pass


class PriorityNode(Node):
    # Constructor
    def __init__(self, x, y, board, tile):
        # Coordinates
        self.x = x
        self.y = y

        self.tile = tile
        # Reference to the board class
        self.board = board

        # g and f scores
        self.g = 0
        self.f = 0

        # Heuristic function
        self.h = lambda x, y: sqrt((self.x-x)**2 + (self.y-y)**2)
        # self.h = lambda x, y: fabs(x-self.x) + fabs(y-self.y)

        # Priority Queue counter in case equal priority (f)
        self.c = 0

        self.closed = False

        Node.__init__(self, (x, y), board)

    def update_priority(self, goal, c):
        self.c = c
        self.f = self.g + self.h(goal.x, goal.y) * 10  # A*

    def __lt__(self, other):  # comparison method for priority queue
        return self.f + self.c < other.f + self.c

    def __repr__(self):
        return "<Node (x:%s, y:%s, f:%s, c:%s, t:%s)>" % (self.x, self.y, self.f, self.c, self.tile)


class Board(Problem):
    def __init__(self, board):
        self.board = board  # Holds the input board for reference

        self.state = []  # Matrix of board Nodes
        self.open = []  # List of open Nodes
        self.closed = []  # List of closed Nodes

        self.goal = None  # The goal Node
        self.initial = None  # The initial Node

        self.counter = count()  # Unique sequence count for correct priority queue implementation

        # Sizes defining the board
        self.width = 0
        self.height = 0

        # Holds several solution related data instances
        self.solution = {'path': [], 'length': 0, 'found': False, 'steps': 0, 'states': []}

        self.init_state()  # Initialize state

        Problem.__init__(self, self.state, self.initial, self.goal)

    def __repr__(self):
        representation = '<Board ([\n'
        for line in list(self.board):
            representation += line+'\n'
        representation += '], \n'

        representation += 'initial node:  ' + str(self.initial) + '\n'
        representation += 'goal node:     ' + str(self.goal) + '\n)'
        representation += 'open:          ' + str(self.open) + '\n'
        representation += 'closed:        ' + str(self.closed) + '\n'
        representation += 'counter:       ' + str(next(self.counter)) + '\n'
        representation += 'solution path: ' + str(self.solution_path) + '\n'

        return representation

    def init_state(self):
        self.height = len(self.board)-1
        self.width = max(map(len, self.board))-1

        y = -1
        for row in list(self.board):
            node_row = []
            y += 1
            x = -1
            for tile in row:
                x += 1
                if tile != '\n':
                    node = PriorityNode(x, y, self, tile)

                    if tile == 'B':
                        # Goal node is set
                        self.goal = node
                    elif tile == 'A':
                        # Start node is opened
                        self.initial = node
                        self.open.append(node)
                    elif tile == '#':
                        # Walls are closed
                        node.closed = True
                        # self.closed.append(node)

                    node_row.append(node)
            self.state.append(node_row)

    # In our problem, actions are all nodes reachable from current Node within the board matrix
    def actions(self, node):
        try:
            if node.y > 0:  # UP
                child = self.state[node.y-1][node.x]
                if not child.closed:
                    yield child
            if node.y < self.height:  # DOWN
                child = self.state[node.y+1][node.x]
                if not child.closed:
                    yield child
            if node.x > 0:  # LEFT
                child = self.state[node.y][node.x-1]
                if not child.closed:
                    yield child
            if node.x < self.width:  # RIGHT
                child = self.state[node.y][node.x+1]
                if not child.closed:
                    yield child
        except IndexError as e:
            print(e)

    def save_state(self):
        self.solution['states'].append(self.state)

    def add_path(self, path, node):
        path_line = list(path[node.y])
        path_line[node.x] = 'x'
        path[node.y] = "".join(path_line)

        return path

    def solve(self, algorithm):
        path = list(self.board)

        solution_path, steps, found = algorithm(self)

        for node in solution_path:
            path = self.add_path(path, node)

        self.solution['path'] = path
        self.solution['length'] = len(solution_path)
        self.solution['steps'] = steps
        self.solution['found'] = path

    def solution_states_generator(self):
        for state in self.solution['states']:
            yield state

    def pretty_print(self):
        if self.solution['found']:
            print("Solution found in %s steps, solution length is %s" % (self.solution['steps'], self.solution['length']))
        else:
            print("No solution found in %s steps, solution length is %s" % (self.solution['steps'], float('inf')))

        print('_'*len(self.board[0]))
        for solution_line in self.solution['path']:
            print(solution_line)
        print('_'*len(self.board[0]))
        print('')


class PriorityQueue:
    def __init__(self):
        pass

    def add(self, problem, item):
        # Simulated memoization of f(n) = g(n) + h(n)
        if item.f:
            return
        item.update_priority(problem.goal, next(problem.counter))
        heappush(problem.open, item)

    def pop(self, queue):
        return heappop(queue)


class Stack:
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.append(item)

    def pop(self, stack):
        return stack.pop()


class FIFOQueue:
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.append(item)

    def pop(self, queue):
        return queue.pop(0)


def graph_search(problem, frontier):
    path, steps = [], 0
    while problem.open:
        node = frontier.pop(problem.open)
        steps += 1

        if node.closed:
            continue

        path.append(node)
        problem.save_state()

        if problem.goal_test(node):
            return path, steps, True

        for child_node in problem.actions(node):
            if child_node.closed:
                continue

            child_node.parent = node
            frontier.add(problem, child_node)

        # We have explored all the child nodes of this node, so we close it.
        node.closed = True
        # self.closed.append(node)

    return path, steps, False


def a_star(problem):
    return graph_search(problem, PriorityQueue())


def depth_first_search(problem):
    return graph_search(problem, Stack())


def breadth_first_search(problem):
    return graph_search(problem, FIFOQueue())


if __name__ == '__main__':
    G = [
    '..............#.....',
    '..............#.....',
    '.........######.....',
    '...........A..#..B..',
    '.........######.....',
    '..............#.....',
    '....................']

    
    b = Board(list(G))
    b.solve(a_star)
    # b.pretty_print()

    b = Board(list(G))
    b.solve(depth_first_search)
    # b.pretty_print()


    b = Board(list(G))
    b.solve(breadth_first_search)
    # b.pretty_print()



"""

PETER NORVIG:

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


MAGNUS LIE HETLAND:

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
"""