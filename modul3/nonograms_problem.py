import copy
import time
from algorithms.search import Problem
from algorithms.csp import GAC, CSP, Constraint, GACPriorityNode
DEBUG = False


class NonogramProblem(CSP):
    def __init__(self):
        """
        Constructor for the NonogramProblem
        Will set up the grid and create all nodes with all possible permutations as domains
        """
        self.node_domain = {}
        self.constraints = {}

        self.grid = [[]]
        self.total_cols = 0
        self.total_rows = 0

        self.start = None
        self.open = []

        self.init_time = 0

        CSP.__init__(self, self.node_domain, self.constraints)

    def nono_cf(self, x, y):
        """
        Constraint for the Nonogram constraint satisfaction problem.
        The contents of a cell must be the same in both row and column - otherwise it is not a valid constraint.
        :param x: Row with both a row-unique id and its respective cells
        :param y: Column with both a column-unique id its respective cells
        :return: Boolean, signifying if the constraint is upheld by the input.
        """
        r, row = x
        c, col = y
        return row[c] == col[r]

    def set_scenario(self, scenario_filepath):
        """
        Sets scenario for Nonogram problem using a file path as input.
        :param scenario_filepath:
        :return:
        """
        self.init_time = time.time()
        with open(scenario_filepath) as f:
            columns, rows = map(int, f.readline().split())

            self.grid = [[False]*columns]*rows
            self.total_rows = rows
            self.total_cols = columns

            r_reversed = []
            for row in range(rows):
                r_reversed.append(list(map(int, f.readline().split())))
            for row, counts in enumerate(reversed(r_reversed)):
                self.node_domain[row] = [(row, p) for p in self.generate_perm_patterns(counts, columns)]

            for col in range(columns):
                counts = list(map(int, f.readline().split()))

                self.node_domain[rows + col] = [(col, p) for p in self.generate_perm_patterns(counts, rows)]

        self.initialize()

    def initialize(self):
        """
        Initializes problem by setting constraints, and adding an initialized GACNode to the open queue.
        :return:
        """
        self.constraints = {}
        self.set_constraints()

        self.start = GACPriorityNode(self)
        self.start.initialize()
        self.start.domain_filtering()

        if self.is_goal(self.start):
            self.init_time = time.time() - self.init_time
            print("GOOOOOOOOAAAAAAl", self.init_time)

        self.open = [self.start]

    def generate_perm_patterns(self, series, columns):
        """
        Generates pattern permutations for a given number of segments and columns
        :param series: A seies of segment lengths
        :param columns: The number of columns in the nonogram
        :return: A pattern matrix
        """

        # If the length of the series is 0, then False * len(column) will be returned
        if len(series) == 0:
            return [[False for _ in range(columns)]]

        permutations = []
        for start in range(columns - series[0] + 1):
            permutation = []

            permutation += [False for _ in range(start)]
            permutation += [True for _ in range(start, start + series[0])]

            sub_start = start + series[0]
            if sub_start < columns:
                permutation.append(False)
                sub_start += 1

            if sub_start == columns and len(series) == 0:
                permutations.append(permutation)
                break

            sub_rows = self.generate_perm_patterns(series[1:len(series)], columns - sub_start)

            for sub_row in sub_rows:
                sub_permutation = copy.deepcopy(permutation)
                sub_permutation += [sub_row[x - sub_start] for x in range(sub_start, columns)]
                permutations.append(sub_permutation)

        return permutations

    def set_constraints(self):
        """
        Generates constraint network for the problem
        In this problem it is implemented as a dictionary with a given row/col index as a key
        The respective value is a list with the index for all possible rows/columns the row/col has constraints against
        More specific this means a list of all intersecting cells between a row and a column.
        """
        for row in range(self.total_rows):
            self.constraints[row] = Constraint([i for i in range(self.total_rows, self.total_rows + self.total_cols)],
                                               self.nono_cf)
        for col in range(self.total_cols):
            self.constraints[self.total_rows + col] = Constraint([i for i in range(0, self.total_rows)], self.nono_cf)

    def is_goal(self, other):
        return self.h(other) == 0

    def h(self, state):
        """
        Calculates the heuristic for a given state.
        In this Nonogram problem the heuristic is the sum of all the domains in the variables list
        :param state: State which the heuristic is calculated from.
        :return: The heuristic of the state.
        """
        return sum((len(domains) - 1) for domains in state.node_domain.values())

    def path_cost(self, movement):
        return 1
