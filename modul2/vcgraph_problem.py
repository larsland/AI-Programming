from algorithms.csp import Constraint, GAC, CSP
from algorithms.search import Problem
from algorithms.utils import UniversalDict
import copy


# PriorityNode
class VCGACNode(GAC):
    def __init__(self, csp, node_domain_map, problem, constraints, coordinates):
        self.csp = csp
        self.coordinates = coordinates
        self.problem = problem
        self.f = 0

        GAC.__init__(self, csp)

    def __lt__(self, other):
        return self.f < other.f


class VertexColoringProblem(CSP):
    def __init__(self):
        self.coordinates = {}
        self.node_domain_map = {}
        self.constraints = []

        self.start = VCGACNode(self, self.node_domain_map, self, self.constraints, self.coordinates)
        self.start.initialize()
        self.start.domain_filtering()
        self.open = [self.start]

        CSP.__init__(self, self.node_domain_map, self.constraints)

    def set_graph(self, graph=open('modul2/graph1.txt'), dom_size=4):
        ls = graph.read().splitlines()
        nv, ne = map(int, ls[0].split())

        for s in ls[1:nv+1]:
            index, x, y = map(eval, s.split())
            self.coordinates[index] = [x, y]
            self.node_domain_map[index] = [i for i in range(dom_size)]

        for s in ls[nv+1:]:
            n, m = map(int, s.split())
            self.constraints.append(Constraint([n, m], lambda x, y: x != y))

    def initialize(self):
        self.set_graph()

    def save_state(self):
        pass

    '''
    def save_state2(self):
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
        self.solution.states.append(state)
    '''

    def path_cost(self, movement):
        return 1

    def actions(self, state):
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

    def h(self, state):
        return sum(len(d)-1 for d in state.node_domain_map.values())

    def is_goal(self, state):
        return all(map(lambda d: len(d) == 1, state.node_domain_map.values()))

    def make_func(self, var_names, expression):
        args = ""
        for n in var_names:
            args += "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")")

    def get_input(self):
        " From file and asks K from user. "
        f = open('modul2/graph2.txt', "r")
        ls = f.read().splitlines()
        nv, ne = map(int, ls[0].split())

        K = int(input("K = "))

        for s in ls[1:nv+1]:
            index, x, y = map(eval, s.split())
            self.coordinates[index] = [x, y]
            self.node_domain_map[index] = [i for i in range(K)]

        for s in ls[nv+1:]:
            n, m = map(int, s.split())
            self.constraints.append(Constraint([n, m], lambda x, y: x != y))

    def solve(self, algorithm):
        print(algorithm(self))