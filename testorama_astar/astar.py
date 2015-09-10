from heapq import heappush, heappop
from collections import deque
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
        """General goal test to see if goal has been achieved"""
        return self.goal == other

    def save_state(self):
        """Useful when you want to review the states your algorithm created"""
        pass


class PriorityNode(Node):
    """This node is specialized to be used in the context of a priority heap (or queue).
    The order of nodes is derived from the comparison method __lt__, based on priority, as seen below.
    For the purpose of this task the priority is calculated from f(n) = g(n) + h(n).
    """

    def __init__(self, x, y, board, tile):
        # Coordinates
        self.x = x
        self.y = y

        self.tile = tile    # 'A', 'B', '.' or '#'
        self.board = board  # Reference to the board class

        # g and f scores
        self.g = 0
        self.f = 0

        # Heuristic function with euclidean distance.
        self.h = lambda x, y: sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        # Heuristic function with manhattan distance.
        # self.h = lambda x, y: fabs(x-self.x) + fabs(y-self.y)

        self.c = 0              # Priority Queue counter in case equal priority (f)
        self.closed = False     # Use this to check if the node has been traversed.

        Node.__init__(self, (x, y), board)

    def update_priority(self, goal, c):
        self.c = c
        self.f = self.g + self.h(goal.x, goal.y) * 10  # A*

    def __lt__(self, other):
        """Comparison method for priority queue"""
        return self.f + self.c < other.f + self.c

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<Node (x:%s, y:%s, f:%s, c:%s, t:%s)>" % (self.x, self.y, self.f, self.c, self.tile)


class Board(Problem):
    """The problem in this task is a matrix of nodes, which can be thought of as a board.
    This board problem contains the variables needed to represent this matrix, and the
    methods needed to allow an algorithm to solve it. This includes the problem
    initialization and the generation of possible actions for the current state."""

    def __init__(self, board):
        self.board = board      # Holds the input board for reference
        self.state = []         # Matrix of board Nodes
        self.open = []          # List of open Nodes
        self.goal = None        # The goal Node
        self.initial = None     # The initial Node
        self.counter = count()  # Unique sequence count for correct action priority

        # Sizes defining the board
        self.width = 0
        self.height = 0

        # Holds several solution related data instances
        self.solution = {'path': [], 'length': 0, 'found': False, 'steps': 0, 'states': []}

        # Initialize super class
        Problem.__init__(self, self.state, self.initial, self.goal)

    def __repr__(self):
        """Representation method for printing a Board with valuable information"""
        representation = '<Board ([\n'
        for line in list(self.board):
            representation += line + '\n'
        representation += '], \n'

        representation += 'initial node:  ' + str(self.initial) + '\n'
        representation += 'goal node:     ' + str(self.goal) + '\n)'
        representation += 'open:          ' + str(self.open) + '\n'
        representation += 'counter:       ' + str(next(self.counter)) + '\n'
        representation += 'solution path: ' + str(self.solution['path']) + '\n'

        return representation

    def init_state(self):
        """Initialize the problem state by feeding the problem through a set of rules """
        self.height = len(self.board) - 1                   # Get the height and width of the problem
        self.width = max(map(len, self.board)) - 1

        y = -1
        for row in list(self.board):                        # For each row in the board
            node_row = []
            y += 1
            x = -1
            for tile in row:                                # For each tile in the board row
                x += 1
                if tile != '\n':                            # If tile not a line break then
                    node = PriorityNode(x, y, self, tile)   # create the PriorityNode based on position and tile value.

                    if tile == 'B':                         # If tile has value of B then
                        self.goal = node                    # set this node as the goal node.
                    elif tile == 'A':                       # If tile has value of A then
                        self.initial = node                 # set this node as start node and
                        self.open.append(node)              # add it to the open set.
                    elif tile == '#':                       # If tile has value of # then
                        node.closed = True                  # close the node as it can not be accessed.

                    node_row.append(node)                   # Add node to current row of nodes and
            self.state.append(node_row)                     # add row of nodes to the problem state.

    def actions(self, node):
        """In our problem, actions are all nodes reachable from current Node within the board matrix"""
        if node.y > 0:
            yield self.state[node.y - 1][node.x]    # Up
        if node.y < self.height:
            yield self.state[node.y + 1][node.x]    # Down
        if node.x > 0:
            yield self.state[node.y][node.x - 1]    # Left
        if node.x < self.width:
            yield self.state[node.y][node.x + 1]    # Right

    def add_path(self, path, node):
        path_line = list(path[node.y])
        path_line[node.x] = 'x'
        path[node.y] = "".join(path_line)

        return path

    def solve(self, algorithm):
        """Problem solver that takes in a selected algorithm and
        formats the response in a handy way via our solution dictionary"""
        path = list(self.board)

        solution_path, steps, found = algorithm(self)

        for node in solution_path:
            path = self.add_path(path, node)

        self.solution['path'] = path
        self.solution['length'] = len(solution_path)
        self.solution['steps'] = steps
        self.solution['found'] = path

    def save_state(self):
        """For storing states as the algorithm traverses the problem"""
        self.solution['states'].append(self.state)

    def solution_states_generator(self):
        """Generator for all the solution states"""
        for state in self.solution['states']:
            yield state

    def pretty_print(self):
        """Helper method for beautiful printing of the problem solution"""
        if self.solution['found']:
            print(
                "Solution found in %s steps, solution length is %s" % (self.solution['steps'], self.solution['length']))
        else:
            print("No solution found in %s steps, solution length is %s" % (self.solution['steps'], float('inf')))

        print('_' * len(self.board[0]))
        for solution_line in self.solution['path']:
            print(solution_line)
        print('_' * len(self.board[0]))
        print('')


class PriorityQueue:
    def __init__(self):
        pass

    def add(self, problem, node):
        # Simulated memoization of f(n) = g(n) + h(n)
        if node.f:
            return

        # Update the priority of the node based on its proximity to the goal
        # as well as a tie-breaker in the form of a counter.
        node.update_priority(problem.goal, next(problem.counter))
        # Push node onto heap
        heappush(problem.open, node)

    def pop(self, queue):
        # Use heappop to retrieve node with highest priority
        return heappop(queue)


class LIFOQueue:
    # Also known as a Stack
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.appendleft(item)  # First in

    def pop(self, queue):
        return queue.popleft()  # Last out


class FIFOQueue:
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.appendleft(item)  # First in

    def pop(self, queue):
        return queue.pop()  # First out


def graph_search(problem, frontier):
    """ A normal Graph search contains all the necessary tools to implement the three algorithms
     specified in the task."""
    problem.init_state()                            # Initialize problem state
    path, steps = [], 0                             # Containers for path and amount of steps taken
    while problem.open:                             # While there are still nodes in the queue
        node = frontier.pop(problem.open)           # Pop node
        steps += 1                                  # Increment steps taken

        if node.closed:                             # If node has been closed then
            continue                                # skip to next iteration

        path.append(node)                           # Save path and
        problem.save_state()                        # current state

        if problem.goal_test(node):                 # Is current node the goal node? Then
            return path, steps, True                # end algorithm and return result

        for child_node in problem.actions(node):    # For each child node reachable from the current node,
            if child_node.closed:                   # if child node has been closed then
                continue                            # skip to next iteration

            frontier.add(problem, child_node)       # Add child to list of open nodes

        node.closed = True                          # All the child nodes of this node have been explored so we close it
        # Alternative: self.closed.append(node)

    return path, steps, False                       # End algorithm and return result


def a_star(problem):
    """A* is a graph search with a heuristic.
    In our implementation we use our Priority Nodes
    with their heuristic as well as a PriorityQueue
    to implement the A* algorithm."""
    return graph_search(problem, PriorityQueue())


def depth_first_search(problem):
    """Depth first search is a graph search
    where the open nodes are on a Last In First Out queue (LIFO),
    also known as a Stack"""
    problem.open = deque()
    return graph_search(problem, LIFOQueue())


def breadth_first_search(problem):
    """Depth first search is a graph search
    where the open nodes are on a First In first Out queue (LIFO)"""
    problem.open = deque()
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
    b.pretty_print()

    b = Board(list(G))
    b.solve(depth_first_search)
    b.pretty_print()

    b = Board(list(G))
    b.solve(breadth_first_search)
    b.pretty_print()

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

from functools import wraps
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