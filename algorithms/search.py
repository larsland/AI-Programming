from heapq import heappush, heappop
from collections import deque
import math


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
        return hash(str(self.state))


class Problem():
    def __init__(self, state, initial, goal=None):
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

    def __init__(self, node_x, node_y, board, tile):
        # Coordinates
        self.x = node_x
        self.y = node_y

        self.tile = tile    # 'A', 'B', '.' or '#'
        self.board = board  # Reference to the board class

        # g and f scores
        self.g = 0
        self.f = 0

        # Heuristic function with euclidean distance.
        self.h = lambda x, y: math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        # Heuristic function with manhattan distance.
        # self.h = lambda x, y: fabs(x-self.x) + fabs(y-self.y)

        self.c = 0              # Priority Queue counter in case equal priority (f)
        self.closed = False     # Use this to check if the node has been traversed.

        Node.__init__(self, (node_x, node_y), board)

    def update_priority(self, goal, c):
        self.c = c
        self.f = self.g + self.h(goal.x, goal.y) * 10  # A*

    def __lt__(self, other):
        """Comparison method for priority queue"""
        return self.f + self.c < other.f + self.c

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<Node (x:%s, y:%s, f:%s, c:%s, t:%s)>" % (self.x, self.y, self.f, self.c, self.tile)


class Agenda:
    """ Also known as a priority queue """
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


class LIFO:
    """ Also known as a stack """
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.append(item)  # Last in

    def pop(self, queue):
        return queue.pop()  # First out


class FIFO:
    """ Also known as a queue """
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

        if node.closed:                             # If node has been closed then
            continue                                # skip to next iteration

        if problem.goal_test(node):                 # Is current node the goal node? Then
            return path, True                # end algorithm and return result

        for child_node in problem.actions(node):    # For each child node reachable from the current node,
            if not child_node.closed:               # if child node has been closed then
                frontier.add(problem, child_node)   # Add child to list of open nodes
        node.closed = True                          # All the child nodes of this node have been explored so we close it

        path.append(node)                           # Save path and
        problem.save_state()                        # current state

    return path, False                       # End algorithm and return result


def a_star(problem):
    """A* is a graph search with a heuristic.
    In our implementation we use our Priority Nodes
    with their heuristic as well as a PriorityQueue
    to implement the A* algorithm."""
    return graph_search(problem, Agenda())


def depth_first_search(problem):
    """Depth first search is a graph search
    where the open nodes are on a Last In First Out queue (LIFO),
    also known as a Stack"""
    problem.open = deque()
    return graph_search(problem, LIFO())


def breadth_first_search(problem):
    """Depth first search is a graph search
    where the open nodes are on a First In first Out queue (LIFO)"""
    problem.open = deque()
    return graph_search(problem, FIFO())


class Bunch(dict):
    """Simple class for prototyping and other handy stuff"""
    def __init__(self, *args, **kwargs):
        super(Bunch, self).__init__(*args, **kwargs)
        self.__dict__ = self