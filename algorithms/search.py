from heapq import heappush, heappop
from algorithms.utils import memoize, Bunch
from abc import abstractclassmethod


class Problem:
    def __init__(self, state, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.state = state
        self.goal = goal
        # Holds several solution related data instances
        self.solution = Bunch(path=[], length=0, found=False, steps=0, states=[])

    @abstractclassmethod
    def initialize(self):
        """Initialization method for the state of the problem,
        can be a list, matrix, tree or any other data structure that fits the problem"""
        pass

    @abstractclassmethod
    def actions(self, state):
        """Returns all actions that can be performed from current state,
        either as a data structure or a generator"""
        pass

    @abstractclassmethod
    def solve(self, algorithm):
        """Solve the problem with the given algorithm"""
        pass

    @abstractclassmethod
    def goal_test   (self, other):
        """General goal test to see if goal has been achieved"""
        return self.goal == other

    @abstractclassmethod
    def save_state(self):
        """Useful when you want to review the states your algorithm created"""
        pass

    @abstractclassmethod
    def path_cost(self, movement):
        """Cost of a movement"""
        pass


class Node:
    def __init__(self, state, problem, parent=None, action=None, path_cost=0):
        self.state = state
        self.problem = problem
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.closed = False     # Use this to check if the node has been traversed.

    def __hash__(self):
        return hash(str(self.state))

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<Node (state:%s, action:%s, path_cost:%s, c:%s)>" % (self.state, self.action, self.path_cost,
                                                                     self.closed)

    def path(self):
        path = []
        node = self
        while node.parent:
            path.append(node)
            node = node.parent
        return path


# PriorityNode
class PriorityNode(Node):
    """This node is specialized to be used in the context of a priority heap (or queue).
    The order of nodes is derived from the comparison method __lt__, based on priority, as seen below.
    For the purpose of this task the priority is calculated from f(n) = g(n) + h(n).
    """
    def __init__(self, state, problem, path_cost=1):
        self.g = path_cost
        self.f = 0

        Node.__init__(self, state, problem, path_cost=path_cost)

    def __lt__(self, other):
        """Comparison method for priority queue"""
        return self.f < other.f

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<PriorityNode (f:%s, g:%s, h:%s, state:%s, closed:%s)>" % \
               (self.f, self.g, self.problem.h(self), self.state, self.closed)


class Agenda:
    """ Also known as a priority queue """
    def __init__(self):
        pass

    @staticmethod
    def add(queue, node):
        # Push node onto heap
        heappush(queue, node)

    @staticmethod
    def pop(queue):
        # Use heappop to retrieve node with highest priority
        return heappop(queue), queue

    @staticmethod
    def contains(item, queue):
        return item in queue


class LIFO:
    """ Also known as a stack """
    def __init__(self):
        pass

    @staticmethod
    def add(_open, item):
        _open.append(item)  # Last in

    @staticmethod
    def pop(queue):
        return queue.pop(), queue  # First out

    @staticmethod
    def contains(item, queue):
        return item in queue


class FIFO:
    """ Also known as a queue """
    def __init__(self):
        pass

    @staticmethod
    def add(_open, item):
        _open.appendleft(item)  # First in

    @staticmethod
    def pop(queue):
        return queue.pop(), queue  # First out

    @staticmethod
    def contains(item, queue):
        return item in queue


class GraphSearch:
    def __init__(self, problem, frontier):
        self.problem = problem
        self.frontier = frontier()
        self.open, self.closed, self.path, self.came_from = [], [], [], {}

        self.is_closed = memoize(lambda node: node in self.closed)

        # Initializing
        self.g = {self.problem.start: 0}
        self.frontier.add(self.open, self.problem.start)

    def search(self):
        """
        A general algorithm for A*, dfs and bfs search.
        :param problem: The problem instance that this graph searcher will try to solve
        :param frontier: Class which holds methods to interact with the data structure of open nodes
        :return: Path to goal and indicator of success
        """
        _open, closed, path = self.open, self.closed, self.path
        problem, g, frontier = self.problem, self.g, self.frontier
        is_closed = self.is_closed

        while _open:
            node, _open = frontier.pop(_open)
            closed.append(node)
            #problem.save_state(node)
            path.append(node)
            if problem.is_goal(node):
                print("MADDAFAKINNS SUCCESS!!!!!")
                return self.path, True
            for child in problem.actions(node):
                new_g = g[node] + problem.path_cost((node, child))
                if is_closed(child):
                    continue
                in_open = frontier.contains(child, _open)
                if not in_open or (child in g and new_g < g[child]):
                    g[child] = new_g
                    child.f = new_g + problem.h(child)
                    self.came_from[child] = node
                    if not in_open:
                        frontier.add(_open, child)

        return [], False

    def search_yieldie(self):
        """
        A general algorithm for A*, dfs and bfs search.
        :param problem: The problem instance that this graph searcher will try to solve
        :param frontier: Class which holds methods to interact with the data structure of open nodes
        :return: Path to goal and indicator of success
        """
        _open, closed, path = self.open, self.closed, self.path
        problem, g, frontier = self.problem, self.g, self.frontier
        is_closed = self.is_closed
        solved = False

        while _open:
            node, _open = frontier.pop(_open)
            closed.append(node)
            #problem.save_state(node)

            yield {
                'node': node,
                'open': len(self.open),
                'closed': len(self.closed),
                'solved': None
            }

            # yield node
            if problem.is_goal(node):
                solved = True
                break
            for child in problem.actions(node):
                new_g = g[node] + problem.path_cost((node, child))
                if is_closed(child):
                    continue
                in_open = frontier.contains(child, _open)
                if not in_open or (child in g and new_g < g[child]):
                    g[child] = new_g
                    child.f = new_g + problem.h(child)
                    self.came_from[child] = node
                    if not in_open:
                        frontier.add(_open, child)

        yield {
            'solved': solved
        }



    def reconstruct_path(self, path):
        " Reconstructs path from goal to start node. "
        while path[-1] != self.problem.start:
            path.append(self.came_from[path[-1]])
        return path[::-1]