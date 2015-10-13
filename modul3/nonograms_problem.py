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
        self.node_domain_map = {}
        self.constraints = {}

        self.grid = [[]]
        self.total_cols = 0
        self.total_rows = 0

        def cf(a, b):
            r, domain_a = a
            c, domain_b = b

            return domain_a[c] == domain_b[r]

        self.cons = lambda x, y: cf(x, y)

        self.start = NonoGACNode(self)
        self.start.initialize()
        self.start.domain_filtering()
        self.open = [self.start]

        CSP.__init__(self, self.node_domain_map, self.constraints)

    def set_scenario(self, scenario):
        with open(scenario) as f:
            cols, rows = map(int, f.readline().split())

            self.grid = [[False]*cols]*rows
            self.total_rows = rows
            self.total_cols = cols

            r_reversed = []
            for row in range(rows):
                r_reversed.append(list(map(int, f.readline().split())))
            for row, counts in enumerate(reversed(r_reversed)):
                self.node_domain_map[row] = [(row, p) for p in self.gen_patterns(counts, cols)]

            for col in range(cols):
                counts = list(map(int, f.readline().split()))
                self.node_domain_map[rows + col] = [(col, p) for p in self.gen_patterns(counts, rows)]

        if DEBUG:
            for x in range(rows + cols):
                print(self.node_domain_map[x])

        self.constraints = {}
        self.generate_constraints()

        self.start = NonoGACNode(self)
        self.start.initialize()
        self.start.domain_filtering()
        self.open = [self.start]

    @staticmethod
    def gen_patterns(counts, cols):
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

            permutation.extend([False for _ in range(start)])
            permutation.extend([True for _ in range(start, start + counts[0])])

            x = start + counts[0]
            if x < cols:
                permutation.append(False)
                x += 1
            if x == cols and len(counts) == 0:
                permutations.append(permutation)
                break

            sub_start = x
            sub_rows = NonogramProblem.gen_patterns(counts[1:len(counts)], cols - sub_start)

            for sub_row in sub_rows:
                sub_permutation = copy.deepcopy(permutation)

                sub_permutation.extend([sub_row[x - sub_start] for x in range(sub_start, cols)])

                permutations.append(sub_permutation)

        return permutations

    def generate_constraints(self):
        """
        Generates constraint network for the problem
        In this problem it is implemented as a dictionary with a given row/col index as a key
        The respective value is a list with the index for all possible rows/columns the row/col has constraints against
        More specific this means a list of all intersecting cells between a row and a column.
        """

        for row in range(self.total_rows):
            self.constraints[row] = Constraint([i for i in range(self.total_rows, self.total_rows + self.total_cols)])

        for col in range(self.total_cols):
            self.constraints[self.total_rows + col] = Constraint([i for i in range(0, self.total_rows)])

    def get_start_node(self):
        """
        Returns the start node for this problem instance
        :return: the initial state in this specific problem
        """
        return self.start

    def is_goal(self, other):
        return sum((len(domains) - 1) for domains in other.node_domain_map.values()) == 0

    def h(self, state):
        """
        Calculates the heuristic for a given state
        In this problem the heuristic is calculated from the sum of all domains in the variables list
        :param astar_state: The state to calculate h for
        :return: The h value
        """
        h = sum((len(domains) - 1) for domains in state.node_domain_map.values())
        return h

    def actions(self, state):
        """
        Fetches all successor nodes from a given CSP state
        In this spesific problem that means all states with a domain
        length greater than 1 for a random node
        :return: The generated successor nodes
        """
        # Generates children and runs the rerun method.
        actions = []
        for node, dom in state.node_domain_map.items():
            if len(dom) > 1:
                for j in range(len(dom)):
                    child = copy.deepcopy(state)
                    child.node_domain_map[node] = [dom[j]]
                    child.rerun(node)
                    if not child.contradiction:
                        actions.append(child)
                return actions
        return actions

    def path_cost(self, movement):
        return 1
