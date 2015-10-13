import copy
from algorithms.search import Problem, PriorityNode
from algorithms.csp import GAC, CSP, Constraint
DEBUG = False


class NonoGACNode(GAC, PriorityNode):
    def __init__(self, csp):
        GAC.__init__(self, csp)
        PriorityNode.__init__(self, csp, csp)


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

        self.start = NonoGACNode(self)
        self.start.initialize()
        self.start.domain_filtering()
        self.open = [self.start]

        CSP.__init__(self, self.node_domain, self.constraints)

    def cons(self, x, y):
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

    def set_scenario(self, scenario='modul3/scenarioes/0-heart.txt'):
        with open(scenario) as f:
            cols, rows = map(int, f.readline().split())

            self.grid = [[False]*cols]*rows
            self.total_rows = rows
            self.total_cols = cols

            r_reversed = []
            for row in range(rows):
                r_reversed.append(list(map(int, f.readline().split())))
            for row, counts in enumerate(reversed(r_reversed)):
                self.node_domain[row] = [(row, p) for p in self.generate_perm_patterns(counts, cols)]

            for col in range(cols):
                counts = list(map(int, f.readline().split()))
                self.node_domain[rows + col] = [(col, p) for p in self.generate_perm_patterns(counts, rows)]

        if DEBUG:
            for x in range(rows + cols):
                print(self.node_domain[x])

        self.constraints = {}
        self.set_constraints()

        self.start = NonoGACNode(self)
        self.start.initialize()
        self.start.domain_filtering()
        self.open = [self.start]

    def generate_perm_patterns(self, counts, cols):
        """
        Generates pattern permutations for a given number of segments
        :param counts: A sequence of segment sizes
        :param cols: The number of columns in the matrix
        :return: A pattern matrix
        """

        if len(counts) == 0:
            return [[False for _ in range(cols)]]

        permutations = []

        for start in range(cols - counts[0] + 1):
            permutation = []

            permutation += [False for _ in range(start)]
            permutation += [True for _ in range(start, start + counts[0])]

            sub_start = start + counts[0]
            if sub_start < cols:
                permutation.append(False)
                sub_start += 1

            if sub_start == cols and len(counts) == 0:
                permutations.append(permutation)
                break

            sub_rows = self.generate_perm_patterns(counts[1:len(counts)], cols - sub_start)

            for sub_row in sub_rows:
                sub_permutation = copy.deepcopy(permutation)
                sub_permutation += [sub_row[x - sub_start] for x in range(sub_start, cols)]
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
                                               self.cons)
        for col in range(self.total_cols):
            self.constraints[self.total_rows + col] = Constraint([i for i in range(0, self.total_rows)], self.cons)

    def is_goal(self, other):
        return sum((len(domains) - 1) for domains in other.node_domain.values()) == 0

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
