import time
from algorithms.csp import Constraint, CSP
from modul2.csp import GACPriorityNode


class VertexColoringProblem(CSP):
    def __init__(self):
        self.coordinates = {}
        self.node_domain = {}
        self.constraints = []

        self.init_time = 0
        self.start = None
        self.open = []

        self.vc_cons = lambda x, y: x != y

        CSP.__init__(self, self.node_domain, self.constraints)

    def set_graph(self, graph='graph.txt', dom_size=4):
        dom_size = int(dom_size)
        lines = open('modul2/graphs/' + graph).read().splitlines()
        nv, ne = map(int, lines[0].split())

        for s in lines[1:nv+1]:
            index, x, y = map(eval, s.split())
            self.coordinates[index] = [x, y]
            self.node_domain[index] = [int(i) for i in range(dom_size)]

        self.constraints = []

        i = 0
        for s in lines[nv+1:]:
            n, m = map(int, s.split())
            self.constraints.append(Constraint([n, m], self.vc_cons))
            i += 1

        self.start = GACPriorityNode(self)
        self.start.initialize()
        self.start.domain_filtering()

        if self.is_goal(self.start):
            self.init_time = time.time() - self.init_time

        self.open = [self.start]

    def path_cost(self, movement):
        return 1

    def h(self, state):
        return sum(len(d)-1 for d in state.node_domain.values())

    def is_goal(self, state):
        return all(map(lambda d: len(d) == 1, state.node_domain.values()))

    def make_func(self, var_names, expression):
        args = ""
        for n in var_names:
            args += "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")")