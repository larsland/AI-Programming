from algorithms.csp import Constraint, GAC, CSP
from algorithms.search import Problem
from algorithms.utils import UniversalDict
import copy


class Node:
    def __init__(self, state, problem, parent=None, action=None, path_cost=0):
        self.state = state
        self.problem = problem
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.closed = False     # Use this to check if the node has been traversed.

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


# PriorityNode
class PriorityNode(Node):
    """This node is specialized to be used in the context of a priority heap (or queue).
    The order of nodes is derived from the comparison method __lt__, based on priority, as seen below.
    For the purpose of this task the priority is calculated from f(n) = g(n) + h(n).
    """
    def __init__(self, state, problem, path_cost=1):
        self.g = path_cost
        self.f = 0

        Node.__init__(self, state, problem, path_cost=path_cost)

    def __lt__(self, other):
        """Comparison method for priority queue"""
        return self.f < other.f

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<PriorityNode (f:%s, g:%s, h:%s, state:%s, closed:%s)>" % \
               (self.f, self.g, self.problem.h(self), self.state, self.closed)


class GACPriorityNode(GAC, PriorityNode):
    def __init__(self, csp):
        GAC.__init__(self, csp)
        PriorityNode.__init__(self, None, csp)


class VertexColoringProblem(CSP):
    def __init__(self):
        self.coordinates = {}
        self.node_domain_map = {}
        self.constraints = []

        self.start = GACPriorityNode(self)
        self.start.initialize()
        self.start.domain_filtering()
        self.open = [self.start]

        CSP.__init__(self, self.node_domain_map, self.constraints)

    def set_graph(self, graph='graph1.txt', dom_size=4):
        dom_size = int(dom_size)
        lines = open('modul2/' + graph).read().splitlines()
        nv, ne = map(int, lines[0].split())

        for s in lines[1:nv+1]:
            index, x, y = map(eval, s.split())
            self.coordinates[index] = [x, y]
            self.node_domain_map[index] = [int(i) for i in range(dom_size)]

        for s in lines[nv+1:]:
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
    """
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
    """
    def solve(self, algorithm):
        print(algorithm(self))