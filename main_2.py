from modul2.gui import Gui
from tkinter import *
from algorithms.search import Problem, PriorityNode, Node, a_star
from algorithms.utils import memoize, HashableList, Bunch
import copy

import itertools
count = itertools.count()

class VCNode(Node):
    def __init__(self, id, x, y, problem):
        self.id = id
        self.xPos = x
        self.yPos = y
        self.color = "red"
        self.domain = []
        self.choice = None
        self.neighbors = []
        self.constraint = lambda i, j: i != j

        Node.__init__(self, (x, y), problem)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        # return "<VCNode (id:%s, state:%s, color:%s, c:%s, d:%s)>" % (self.id, self.state, self.color, self.closed, self.domain)
        return "<VCNode (id:%s, d:%s, c:%s)>" % (self.id, self.domain, self.choice)


class Constraint:
    def __init__(self, variables, method=None, description=None):
        self.variables = variables
        self.method = method
        self.description = description
        
    def __repr__(self):
        # return "<Constraint (vars:%s, c:%s)>" % (self.variables, self.description or '')
        return ""


class CSP:
    def __init__(self, nodes, domain, constraints):
        self.nodes = nodes
        self.domain = domain
        self.constraints = constraints

    def __repr__(self):
        return "<CSP (n: %s, d: %s, c: %s)>" % (self.nodes, self.domain, self.constraints)

    def prune(self, node, value, removals):
        if value in node.domain:
            node.domain.remove(value)
        if removals is not None:
            removals.append((node, value))

    def get_domain(self, node):
        return node.domain


class GAC(PriorityNode):
    def __init__(self, csp, problem):
        self.csp = csp
        self.revise_queue = []  # revise queue

        self.removals = []
        self.problem = problem

        PriorityNode.__init__(self, self.revise_queue, self.problem)


    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<GAC (f:%s, g:%s, h:%s, revise_q:%s, closed:%s)>" % \
               (self.f(), self.g, self.problem.h(self), self.revise_queue, self.closed)

    def initialization(self):
        for constraint in self.csp.constraints:
            for node_id in constraint.variables:
                self.revise_queue.append((self.csp.nodes[node_id], constraint))

        self.state = copy.deepcopy(self.revise_queue)
        # Print all node-constraint pairs in queue for debugging
        for x in self.revise_queue:
            print(x)

    def domain_filtering(self):
        while self.revise_queue:
            node, con = self.revise_queue.pop()

            if not node.domain:
                break

            print('NODE', node)
            nodes = self.revise(node, con)
            if nodes:
                self.push_pairs(node, con)

    def push_pairs(self, node, con=None):
        for c in self.csp.constraints:
            if node in c.variables and (con is None or c != con):
                for j in c.variables:
                    if j != node:
                        self.revise_queue.append([c, j])

    # @memoize
    def get_neighbors(self, node):
        neighbors = []
        for c in self.csp.constraints:
            neighbor = False
            current = []
            for n_id in c.variables:
                if node.id == n_id:
                    neighbor = True
                else:
                    current.append(n_id)
            if neighbor:
                neighbors += current
        return neighbors

    def get_node(self, id):
        for node, _ in self.revise_queue:
            if node.id == id:
                return node

    def rerun(self, i):
        self.push_pairs(i)
        self.domain_filtering()

    def revise(self, node, con):
        revised = False
        for value in node.domain:                                               # For each possible value in the domain of the node
            for neighbor_id in con.variables:                                   # check against all neighbors on constraint
                neighbor = self.get_node(neighbor_id)                           # get a neighbor node from id

                if node.id != neighbor_id and not con.method(value, neighbor):  # if neighbor is not node and constraint does not hold
                    if value in node.domain:
                        node.domain.remove(value)
                    # self.csp.prune(node, value, self.removals)  # prune neighbor from
                    revised = True
        return revised

"""
class GACStateNode(PriorityNode):
    def __init__(self, gac_state, problem):
        self.state = gac_state
        self.nodes = gac_state.nodes
        PriorityNode.__init__(self, gac_state, problem)

    def __repr__(self):
        # Representation method for printing a Node with valuable information
        return "<GACStateNode (f:%s, g:%s, h:%s, state:%s, closed:%s)>" % \
               (self.f(), self.g, self.problem.h(self), self.state, self.closed)
"""

class VCGraphProblem(Problem):
    def __init__(self, csp):
        self.csp = csp
        self.open = []

        self.h = lambda state: sum(d for d in [len(n.domain)-1 for n, _ in state.revise_queue])

        # Holds several solution related data instances
        self.solution = Bunch(path=[], length=0, found=False, steps=0, states=[])

        Problem.__init__(self, csp)
    """
    def h(self, state):
        len_sum = 0
        for node, d in state.state:
            len_sum += len(node.domain) - 1
        return len_sum
    """

    def __repr__(self):
        return "<VCGraphProblem (csp:%s, open:%s, solution:%s)>" % \
               (self.csp, self.open, self.solution)

    def initialize(self):
        initial = GAC(self.csp, self)
        # initial = GACStateNode(self.gac, self)
        initial.initialization()
        self.open.append(initial)

        # self.goal = len(self.state.nodes)

    # @memoize
    def actions(self, state):
        """Returns all actions that can be performed from current state,
        either as a data structure or a generator"""
        actions = []
        print("actions!")
        for i, c in state.revise_queue:
            _vars = c.variables
            if len(_vars) > 1:
                for var in _vars:
                    if var != i.id:
                        new_state = copy.deepcopy(state)
                        for n in [n for n, _ in new_state.revise_queue if n.id == i.id]:
                            n.domain = [var]
                            n.choice = var
                            print("before", new_state)
                            new_state.rerun(i)
                            print("after", new_state)
                            if n.domain:
                                actions.append(new_state)

        return actions


    def solve(self, algorithm):
        """Solve the problem with the selected algorithm and
        formats the solution with a dictionary"""
        solution_path, found = algorithm(self)

        self.solution.length = len(solution_path)
        self.solution.steps = len(self.solution.states)
        self.solution.found = found
        self.solution.path = solution_path
        return self.solution

    def goal_test(self, other):
        """General goal test to see if goal has been achieved"""
        return False

    def save_state(self):
        """Useful when you want to review the states your algorithm created"""

    def path_cost(self, movement):
        """Cost of a movement"""
        return 1


def get_graph():
    input_graph = input("Select graph (1-6): ")
    input_graph = "graph" + str(input_graph) + ".txt"
    graph = open('modul2/' + input_graph, 'r').read().splitlines()
    return graph


def create_nodes(num_vertices, graph):
    nodes = []
    for i in range(1, num_vertices + 1):
        id, x, y = [i for i in graph[i].split()]
        node = VCNode(int(id), float(x), float(y), graph)
        nodes.append(node)
    return nodes


def set_constraints(num_vertices, graph, con, description):
    constraints = []
    for i in range(num_vertices + 1, len(graph)):
        constraint = Constraint([int(i) for i in graph[i].split()], con, description)
        constraints.append(constraint)
    return constraints


def get_vc_domain(k):
    variable_colors = ['red', 'green', 'blue', 'yellow', 'pink', 'brown', 'purple', 'orange']
    return variable_colors[0:k]


def makefunc(var_names, expression, envir=globals()):
    args = ''
    for n in var_names:
        args += ', ' + n
    return eval('(lambda ' + args[1:] + ': ' + expression + ' ) ', envir)


def init_VCproblem(graph=None):

    var_list = input('vars: ').replace(' ', '').split(',')
    if not var_list or var_list == ['']:
        var_list = ['x', 'y']
    con_func = input('cons: ')
    if not con_func:
        con_func = 'x!=y'
    description = con_func
    constraint = lambda x, y: x != y  # makefunc(var_list, con_func)

    k = input("K-value (3-10): ")
    if not k:
        k = '3'
    k = int(k)
    graph = get_graph()

    num_vertices = int([i for i in graph[0].split()][0])
    num_edges = int([i for i in graph[0].split()][1])

    nodes = create_nodes(num_vertices, graph)
    constraints = set_constraints(num_vertices, graph, constraint, description)

    vc_domain = range(0, k)
    domains = {}
    for node in nodes:
        node.domain = list(vc_domain)

    csp = CSP(nodes, domains, constraints)
    vc = VCGraphProblem(csp)
    vc.solve(a_star)




    """

    var_list = input('vars: ').replace(' ', '').split(',')
    con_func = input('cons: ')
    description = con_func
    constraint = makefunc(var_list, con_func)

    k = int(input("K-value (3-10): "))
    graph = get_graph()

    num_vertices = int([i for i in graph[0].split()][0])
    num_edges = int([i for i in graph[0].split()][1])

    nodes = create_nodes(num_vertices, graph)
    # constraint = memoize(lambda n: n[0] != n[1])
    constraints = set_constraints(num_vertices, graph, constraint, description)

    vc_dom = range(0, k)
    domains = {}
    for node in nodes:
        domains[node] = list(vc_dom)

    csp = CSP(nodes, domains, constraints)


    gac = GAC(csp)
    gac.initialization()
    gac.domain_filtering()


    #for node in csp.nodes:
    #    print(gac.get_neighbors(node))


    #print(gac.get_neighbors(csp.nodes[7]))


    root = Tk()
    app = Gui(csp, master=root)
    app.mainloop()

    """



from algorithms.utils import HashableList
import timeit

@memoize
def long_operation(stuff):
    return len(list(reversed(stuff)))

if __name__ == '__main__':
    init_VCproblem()




