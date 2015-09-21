import copy, math, random
from itertools import count
from algorithms.search import Problem, PriorityNode
from algorithms.utils import memoize


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
        self.h = memoize(lambda node: (abs(node.x - self.goal.x) + abs(node.y - self.goal.y))*(1+1/100))
        #self.h = memoize(lambda node: math.sqrt(abs(node.x - self.goal.x)**2 + abs(node.y - self.goal.y)**2))
        # *= (1.0 + p) where p is p < (minimum cost of taking one step)/(expected maximum path length)
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

    def initialize(self):
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
        actions = []
        x, y = node.x, node.y
        try:
            if node.x < self.width - 1:
                actions.append(self.state[y][x + 1])    # Right
            if node.x > 0:
                actions.append(self.state[y][x - 1])    # Left
            if node.y < self.height:
                actions.append(self.state[y + 1][x])    # Down
            if node.y > 0:
                actions.append(self.state[y - 1][x])    # Up
        except IndexError as e:
            print(e)
            print(node)
            pass

        return actions

    def add_path(self, path, node):
        path_line = list(path[node.y])
        path_line[node.x] = 'x'
        path[node.y] = "".join(path_line)
        return path

    def solve(self, algorithm):
        """Solve the problem with the selected algorithm and
        formats the solution with a dictionary"""
        path = list(self.board)

        solution_path, found = algorithm(self)

        for node in solution_path:
            path = self.add_path(path, node)

        self.solution['length'] = len(solution_path)
        self.solution['steps'] = len(self.solution['states'])
        self.solution['found'] = found
        self.solution['path'] = solution_path
        return self.solution

    def save_state(self):
        """For storing states as the algorithm traverses the problem.
        Saves the open nodes, the current path and the difference between the current state and the previous one."""
        temp_state = set()
        for nodes in self.state:
            temp_set = set()
            for node in nodes:
                # Deep copy of node
                temp_set.add(copy.copy(node))
            # Freeze the set so it becomes hashable
            temp_set = frozenset(temp_set)
            temp_state.add(temp_set)

        if self.solution['states']:
            diff_state = list(temp_state.difference(self.solution['states'][-1]))
        else:
            diff_state = list(temp_state)

        state = {'state': diff_state, 'open': list(self.open), 'path': list(self.board)}
        self.solution['states'].append(state)

    def solution_states_generator(self):
        """Generator for all the solution states"""
        for state in self.solution['states']:
            yield state

    def get_solution_states(self):
        return self.solution['states']

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