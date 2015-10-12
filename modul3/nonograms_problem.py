import copy
from algorithms.search import Problem
from algorithms.csp import GAC, CSP, Constraint
DEBUG = False


class NonoGACNode(GAC):
    def __init__(self, csp):
        GAC.__init__(self, csp)
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


class NonogramProblem(CSP):
    def __init__(self):
        """
        Constructor for the NonogramProblem
        Will set up the grid and create all nodes with all possible permutations as domains
        """
        self.node_domain_map = {}
        self.constraints = []

        self.nono_cons = None
        self.grid = [[]]
        self.total_cols = 0
        self.total_rows = 0

        self.start = NonoGACNode(self)
        self.start.initialize()
        self.start.domain_filtering()
        self.open = [self.start]

        CSP.__init__(self, self.node_domain_map, self.constraints)


    def set_graph(self, graph='graph1.txt', dom_size=4):
        dom_size = int(dom_size)
        lines = open('modul2/' + graph).read().splitlines()
        nv, ne = map(int, lines[0].split())

        coordinates = {}
        for s in lines[1:nv+1]:
            index, x, y = map(eval, s.split())
            coordinates[index] = [x, y]
            self.node_domain_map[index] = [int(i) for i in range(dom_size)]

        for s in lines[nv+1:]:
            n, m = map(int, s.split())
            self.constraints.append(Constraint([n, m], lambda x, y: x != y))

    def set_scenario(self, nonogram='modul3/scenario.txt'):
        def cf(a, b):
            print('aaaaaaaaaaaa', a)
            print('bbbbbbbbbbbb', b)
            r, domain_a = a
            c, domain_b = b
            return self.get_domain(c) == self.get_domain(r)

        self.nono_cons = lambda x, y: True  # print(x, y)  # self.get_domain(tuple(x)) == self.get_domain(tuple(y))

        with open(nonogram) as f:
            cols, rows = map(int, f.readline().split())

            self.grid = [[False]*cols]*rows
            self.total_rows = rows
            self.total_cols = cols

            r_reversed = []
            for row in range(rows):
                r_reversed.append(list(map(int, f.readline().split())))
            for row, counts in enumerate(reversed(r_reversed)):
                self.node_domain_map[row] = [p for p in self.gen_patterns(counts, cols)]

            for col in range(cols):
                counts = list(map(int, f.readline().split()))
                self.node_domain_map[rows + col] = [p for p in self.gen_patterns(counts, rows)]

            #for node in self.node_domain_map.keys():
            #    print("wtf", node)

        if DEBUG:
            for x in range(rows + cols):
                print(self.node_domain_map[x])

        self.constraints = []
        self.generate_constraints()

        self.start = NonoGACNode(self)
        self.start.initialize()
        self.start.domain_filtering()
        self.open = [self.start]

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
            self.constraints.append(Constraint([i for i in range(self.total_rows, self.total_rows + self.total_cols)],
                                               self.nono_cons))
        for col in range(self.total_cols):
            self.constraints.append(Constraint([i for i in range(0, self.total_rows)],
                                               self.nono_cons))

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
        return sum((len(domains) - 1) for domains in state.node_domain_map.values())

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