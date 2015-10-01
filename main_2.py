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

        Node.__init__(self, (x, y), problem)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<VCNode (id:%s, state:%s, color:%s, c:%s)>" % (self.id, self.state, self.color, self.closed)



class Constraint:
    def __init__(self, variables, method=None, description=None):
        self.variables = variables
        self.method = method
        self.description = description
        
    def __repr__(self):
        return "<Constraint (vars:%s, c:%s)>" % (self.variables, self.description or '')


class CSP:
    def __init__(self, nodes, domain, constraints):
        self.nodes = nodes
        self.domain = domain
        self.constraints = constraints

    def __repr__(self):
        return "<CSP (n: %s, d: %s, c: %s)>" % (self.nodes, self.domain, self.constraints)

    def prune(self, node, value, removals):
        node_domain = self.domain[node.id]
        if value in node_domain:
            node_domain.remove(value)
        if removals is not None:
            removals.append((node, value))

    def get_domain(self, node):
        return self.domain[node.id]


class GAC(PriorityNode):
    def __init__(self, csp, problem):
        self.csp = csp
        self.nodes = [] # revise queue
        self.removals = []
        self.problem = problem

        PriorityNode.__init__(self, self.nodes, self.problem)

    def initialization(self):
        for constraint in self.csp.constraints:
            for node_id in constraint.variables:
                self.nodes.append((self.csp.nodes[node_id], constraint))

        self.state = copy.deepcopy(self.nodes)
        # Print all node-constraint pairs in queue for debugging
        for x in self.nodes:
            print(x)

    def domain_filtering(self):
        while self.nodes:
            node, con = self.nodes.pop()


            """

            Wat?

            """
            if not self.csp.domain[node.id]:
                break

            if self.revise(node, con):
                self.push_pairs(node, con)

    def push_pairs(self, node, con=None):
        for c in self.csp.constraints:
            if node in c.variables and (con is None or c != con):
                for j in c.variables:
                    if j != node:
                        self.nodes.append([c, j])

    @memoize
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

    def rerun(self, i):
        self.push_pairs(i)
        self.domain_filtering()

    def revise(self, node, con):
        print('node: %s, domain: %s' % (node, self.csp.domain[node.id]))
        revised = False
        for value in self.csp.domain[node.id]:
            for c_v in con.variables:
                if node != c_v and con.method(value, self.csp.domain[c_v]):
                    self.csp.prune(node, value, self.removals)
                    revised = True
        return revised


class GACStateNode(PriorityNode):
    def __init__(self, gac_state, problem):
        self.state = gac_state
        self.nodes = gac_state.nodes
        PriorityNode.__init__(self, gac_state, problem)

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<GACStateNode (f:%s, g:%s, h:%s, state:%s, closed:%s)>" % \
               (self.f(), self.g, self.problem.h(self), self.state, self.closed)


class VCGraphProblem(Problem):
    def __init__(self, csp):
        self.csp = csp
        self.open = []
        # self.h = memoize(lambda state: sum([len(self.domain[node])-1 for node in state.nodes]))

        # Holds several solution related data instances
        self.solution = Bunch(path=[], length=0, found=False, steps=0, states=[])

        Problem.__init__(self, csp)

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
        for i, c in state.nodes:
            vars = c.variables
            if len(vars) > 1:
                for var in vars:
                    action = copy.deepcopy(state)
                    action.csp.domain[i] = [var]
                    action.rerun(i)
                    print("hello?", action)
                    if action.csp.domain[i]:
                        actions.append(action)
                return actions
        return []

    def h(self, state):
        print(self)
        len_sum = 0
        for node, d in state.nodes:
            len_sum += len(self.csp.domain[node.id]) - 1
            print(node.id, self.csp.domain[node.id])
        print("H:", len_sum)
        return len_sum

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
        return self.goal == self.h(other)

    def save_state(self):
        """Useful when you want to review the states your algorithm created"""
        pass

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
    constraint = makefunc(var_list, con_func)

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
        domains[node.id] = list(vc_domain)

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




