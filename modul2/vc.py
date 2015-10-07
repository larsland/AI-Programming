from algorithms.csp import Constraint, GAC
from algorithms.utils import UniversalDict
import copy


# PriorityNode
class VCGACNode(GAC):
    def __init__(self, nodes, problem, constraints):
        self.nodes = nodes
        self.problem = problem
        self.constraints = constraints
        self.queue = []
        self.contradiction = False
        self.f = 0

        GAC.__init__(self, nodes, nodes, constraints)

    def __lt__(self, other):
        return self.f < other.f


class VCProblem:
    def __init__(self):
        self.points = {}
        self.nodes = {}
        self.constraints = []
        self.get_input()

        self._constraints = UniversalDict(lambda x, y: x != y)

        root = VCGACNode(self.nodes, self, self.constraints)
        root.initialize()
        root.domain_filtering()
        self.start = root

        self.open = [root]

    def initialize(self):
        pass

    def save_state(self):
        pass

    def path_cost(self, movement):
        return 1

    def actions(self, state):
        " Generates children and runs the rerun method. "
        children = []
        for node, dom in state.nodes.items():
            children = []
            if len(dom) > 1:
                for j in range(len(dom)):
                    child = copy.deepcopy(state)
                    child.nodes[node] = [dom[j]]
                    child.rerun(node)
                    if not child.contradiction:
                        children.append(child)
                return children
        return children

    def h(self, state):
        return sum(len(d)-1 for d in state.nodes.values())

    def is_goal(self, state):
        return all(map(lambda d: len(d) == 1, state.nodes.values()))

    def goal_test(self, state):
        return all(map(lambda d: len(d) == 1, state.nodes.values()))

    def make_func(self, var_names, expression):
        args = ""
        for n in var_names:
            args += "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")")

    def get_input(self):
        " From file and asks K from user. "
        f = open('modul2/graph.txt', "r")
        ls = f.read().splitlines()
        nv, ne = map(int, ls[0].split())

        K = int(input("K = "))

        for s in ls[1:nv+1]:
            index, x, y = map(eval, s.split())
            self.points[index] = (x, y)
            self.nodes[index] = [i for i in range(K)]

        for s in ls[nv+1:]:
            n, m = map(int, s.split())
            self.constraints.append(Constraint([n, m], lambda x, y: x != y))

    def solve(self, algorithm):
        print(algorithm(self))

    """
    def make_var(self, l, s):
        " Create variable and adds to list. "
        index, x, y = map(eval, s.split())
        self.points[index] = (x, y)
        self.nodes[index] = [range(self.K)]
        return l

    def make_con(self, l, s):
        " Create constraint and add to list. "
        n, m = map(int, s.split())
        l.append(Constraint([n, m], lambda n: n[0] != n[1]))
        return l


    def create_nodes(self, num_vertices, graph, k=4):
        for i in range(1, num_vertices + 1):
            id, x, y = map(eval, graph[i].split())
            self.points[id] = (x, y)
            rang = [i for i in range(k)]
            self.nodes[id] = [rang]

    def set_constraints(self, num_vertices, graph, con, description):
        for i in range(num_vertices + 1, len(graph)):
            n, m = map(int, graph[i].split())
            constraint = Constraint([n, m], lambda n: n[0] != n[1], description)
            self.constraints.append(constraint)
    """