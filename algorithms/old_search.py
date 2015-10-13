from heapq import heappush, heappop
from collections import deque
from algorithms.utils import memoize, Bunch
import math
from abc import abstractclassmethod


class Node:
    def __init__(self, state, problem, parent=None, action=None, path_cost=0):
        self.state = state
        self.problem = problem
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.closed = False     # Use this to check if the node has been traversed.

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

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


class PriorityNode(Node):
    """This node is specialized to be used in the context of a priority heap (or queue).
    The order of nodes is derived from the comparison method __lt__, based on priority, as seen below.
    For the purpose of this task the priority is calculated from f(n) = g(n) + h(n).
    """
    def __init__(self, state, problem, path_cost=1):
        self.g = path_cost
        self.f = lambda: self.g + self.problem.h(self)

        Node.__init__(self, state, problem, path_cost=path_cost)

    def __lt__(self, other):
        """Comparison method for priority queue"""
        return self.f() < other.f()

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<PriorityNode (f:%s, g:%s, h:%s, state:%s, closed:%s)>" % \
               (self.f(), self.g, self.problem.h(self), self.state, self.closed)


class Agenda:
    """ Also known as a priority queue """
    def __init__(self):
        pass

    def add(self, problem, node):
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
    problem.initialize()                            # Initialize problem state
    while problem.open:                             # While there are still nodes in the queue
        node = frontier.pop(problem.open)           # Pop start node
        if problem.is_goal(node):                 # Is current node the goal node? Then
            return node.path(), True                # end algorithm and return result

        if node.closed:
            continue

        node.closed = True
        for child in problem.actions(node):         # For each child node reachable from the current node,
            if child.closed and node.g + 1 >= child.g:
                continue

            if child not in problem.open or node.g + 1 < child.g:
                child.parent = node
                child.g = node.g + problem.path_cost((node, child))
                if child not in problem.open:
                    child.closed = False
                    frontier.add(problem, child)

            if not child.parent or not child.parent.closed:    # Calling child services.
                child.parent = node

            if not child.closed and child not in problem.open:
                                                    # if child node has been closed then
                frontier.add(problem, child)        # Add child to list of open nodes

        node.closed = True                          # All the child nodes of this node have been explored so we close it
        problem.save_state()                        # current state

    return [], False                       # End algorithm and return result


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