import copy
from algorithms.search import Problem
from algorithms.csp import GAC, CSP
DEBUG = True


class NonogramProblem:
    def __init__(self, path):
        """
        Constructor for the NonogramProblem
        Will set up the grid and create all nodes with all possible permutations as domains
        """

        self.nodes = {}
        with open(path) as f:
            cols, rows = map(int, f.readline().split())

            self.grid = [[False]*cols]*rows
            self.total_rows = rows
            self.total_cols = cols

            r_reversed = []
            for row in range(rows):
                r_reversed.append(list(map(int, f.readline().split())))
            for row, counts in enumerate(reversed(r_reversed)):
                self.nodes[row] = [(row, p) for p in self.gen_patterns(counts, cols)]
            for col in range(cols):
                counts = list(map(int, f.readline().split()))
                self.nodes[rows + col] = [(col, p) for p in self.gen_patterns(counts, rows)]

        if DEBUG:
            for x in range(rows + cols):
                print(self.nodes[x])

        self.constraints = {}
        self.generate_constraints()

        def cf(a, b):
            r, domain_a = a
            c, domain_b = b
            return domain_a[c] == domain_b[r]

        root = GAC(self.nodes, self, self.constraints)
        root.initialize()
        root.domain_filtering()
        self.start = root

        print('NonogramProblem initialized with %dx%d grid' % (rows, cols))

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
            self.constraints[row] = [i for i in range(self.total_rows, self.total_rows + self.total_cols)]
        for col in range(self.total_cols):
            self.constraints[self.total_rows + col] = [i for i in range(0, self.total_rows)]

    def get_start_node(self):
        """
        Returns the start node for this problem instance
        :return: the initial state in this specific problem
        """
        return self.start

    def h(self, state):
        """
        Calculates the heuristic for a given state
        In this problem the heuristic is calculated from the sum of all domains in the variables list
        :param astar_state: The state to calculate h for
        :return: The h value
        """
        h = sum((len(domains) - 1) for domains in state.state.nodes.values())
        if h == 0:
            state.is_goal = True
        return h

    def arc_cost(self, node):
        """
        Returns the arc cost for a given node
        :param node: The node to get arc cost for
        :return: The arc cost, 1 in this implementation
        """
        return 1

    def get_goal_node(self):
        """
        Returns the goal node for the problem instance
        Not implemented for this problem
        :return: None in this instance
        """
        return None

    def actions(self, state):
        """
        Fetches all successor nodes from a given CSP state
        In this spesific problem that means all states with a domain
        length greater than 1 for a random node
        :return: The generated successor nodes
        """

        actions = []
        for node, dom in state.nodes.items():
            if len(dom) > 1:
                for j in range(len(dom)):
                    child = copy.deepcopy(node)
                    child.nodes[node] = [dom[j]]
                    child.rerun(node)

                    if DEBUG:
                        print("Domain for %s is now %s" % (node, str(state.nodes[node])))

                    if not child.contradiction:
                        actions.append(child)

                return actions