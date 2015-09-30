from modul2.gui import Gui
from tkinter import *
from algorithms.search import Problem, PriorityNode, Bunch
from algorithms.utils import memoize
import copy


class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.xPos = x
        self.yPos = y
        self.color = "light blue"

    def __repr__(self):
        return "ID:" + str(self.id)


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
        node_domain = self.domain[node]
        if value in node_domain:
            node_domain.remove(value)
        if removals is not None:
            removals.append((node, value))


class GAC:
    def __init__(self, csp):
        self.csp = csp
        self.revise_queue = []
        self.removals = []

    def initialization(self):
        for constraint in self.csp.constraints:
            for node_id in constraint.variables:
                self.revise_queue.append((self.csp.nodes[node_id], constraint))

        # Print all node-constraint pairs in queue for debugging
        for x in self.revise_queue:
            print(x)

    def domain_filtering(self):
        while self.revise_queue:
            node, con = self.revise_queue.pop()

            if self.revise(node, con):
                self.push_pairs(node, con)

    def push_pairs(self, node, con=None):
        for c in self.csp.constraints:
            if node in c.variables and (con is None or c != con):
                for j in c.variables:
                    if j != node:
                        self.revise_queue.append([c, j])

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
        print('node: %s, domain: %s' % (node, self.csp.domain[node]))
        revised = False
        for value in self.csp.domain[node]:
            for c_v in con.variables:
                if node != c_v and con.method(value, c_v):
                    self.csp.prune(node, value, self.removals)
                    revised = True
        return revised



class GACNode(PriorityNode):
    def __init__(self, problem):
        self.state = problem.state

        PriorityNode.__init__(self, None, None, problem, None)


class VCGraphProblem(Problem, CSP):
    def __init__(self):
        self.state = []
        self.open = []
        # self.h = lambda state: sum([len(self.domain[node])-1 for node in state.nodes])

        Problem.__init__(self, self.state, self.open)

    def h(self, state):
        len_sum = 0
        for node in state.nodes:
            len_sum += self.domain[node] - 1
        return len_sum

    def initialize(self):
        """Initialization method for the state of the problem,
        can be a list, matrix, tree or any other data structure that fits the problem"""
        pass

    def actions(self, state):
        """Returns all actions that can be performed from current state,
        either as a data structure or a generator"""
        actions = []
        for i, d in state.nodes:
            if len(d) > 1:
                children = []
                for j in range(len(d)):
                    child = copy.deepcopy(state)
                    child.nodes[i] = [d[j]]
                    child.rerun(i)
                    if not child.contra:
                        children.append(child)
                return actions
        return []

    def solve(self, algorithm):
        """Solve the problem with the given algorithm"""
        pass

    def goal_test(self, other):
        """General goal test to see if goal has been achieved"""
        return self.goal == other

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
        node = Node(int(id), float(x), float(y))
        nodes.append(node)
    return nodes

#GAC -> memoize(lambda n: n[0]!=n[1])
#constraint = Constraint(i, GAC.method)


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


def init_VCproblem():
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

    for node in csp.nodes:
        print(gac.get_neighbors(node))

    root = Tk()
    app = Gui(csp, master=root)
    app.mainloop()

import ast
if __name__ == '__main__':
    init_VCproblem()


'''

class Constraint():

    method = None

    def __init__(self):
        self.vars = []
        


> [x,y,z], x + y <= z

y i Dy som != x i Dx
lambda n: return n[0] != n[1]


def makefunc(variables, expression, envir=globals()):
    return eval('(lambda ' + ','.join(variables)[:1] + ': ' + expression + ')', envir)
        
        
        
Constraint.method = staticmethod(makefunc(['n'], 'n[0] != n[1]'))


def revise(self, node, constraint):
        new_domain = []
        for domain_node in node.domain:
            valid_domain = False
            for constraint_node in constraint.vars:
                if constraint_node != node:
                    for d in constraint_node.domain:
                        if constraint.method([domain_node, d]):
                            valid_domain = True
                            break

            if valid_domain:
                new_domain.append(domain_node)

        node.domain = new_domain
        
def zebra_constraint(A, a, B, b, recurse=0):
        same = (a == b)
        next_to = abs(a - b) == 1
        if A == 'Englishman' and B == 'Red': return same
        if A == 'Spaniard' and B == 'Dog': return same
        if A == 'Chesterfields' and B == 'Fox': return next_to
        if A == 'Norwegian' and B == 'Blue': return next_to
        if A == 'Kools' and B == 'Yellow': return same
        if A == 'Winston' and B == 'Snails': return same
        if A == 'LuckyStrike' and B == 'OJ': return same
        if A == 'Ukranian' and B == 'Tea': return same
        if A == 'Japanese' and B == 'Parliaments': return same
        if A == 'Kools' and B == 'Horse': return next_to
        if A == 'Coffee' and B == 'Green': return same
        if A == 'Green' and B == 'Ivory': return (a - 1) == b
        if recurse == 0: return zebra_constraint(B, b, A, a, 1)
        if ((A in Colors and B in Colors) or
            (A in Pets and B in Pets) or
            (A in Drinks and B in Drinks) or
            (A in Countries and B in Countries) or
            (A in Smokes and B in Smokes)): return not same        
        raise 'error'


        
'''
