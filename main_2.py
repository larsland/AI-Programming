from modul2.gui import Gui
from tkinter import *
from algorithms.search import Problem
from algorithms.utils import memoize

class Node:
    def __init__(self, index):
        self.index = index
        self.xPos = 0.0
        self.yPos = 0.0
        self.domain = []
        self.color = "black"

    def __repr__(self):
        return "ID:" + str(self.index)


class Constraint:
    def __init__(self, variables, method=None, description=None):
        self.variables = variables
        self.method = method
        self.description = description
        
    def __repr__(self):
        return "<Constraint (variables:%s, constraint:%s)>" % (self.variables, self.description or '')


class CSP(Problem):
    def __init__(self, nodes, domain, constraints):
        self.nodes = nodes
        self.domain = domain
        self.constraints = constraints

        Problem.__init__(self, (nodes, domain, constraints), (nodes, domain, constraints))

    def __repr__(self):
        return "Nodes: " + str(self.nodes) + '\n' + "Domain: " + str(self.domain) + '\n' + \
               "Constraints: " + str(self.constraints)
'''
    def prune(self, var, value, removals):
        # Rule out var=value.
        self.domain[var].remove(value)
        if removals is not None:
            removals.append((var, value))
'''


class GAC:
    def __init__(self, csp):
        self.csp = csp
        self.queue = []
        self.removals = []

    def initialization(self):
        for constraint in self.csp.constraints:
            for var in constraint.variables:
                self.queue.append((self.csp.nodes[var], constraint))

        # Print all node-constraint pairs in queue for debugging
        for x in self.queue:
            print(x)

    def domain_filtering(self):
        while self.queue:
            var, con = self.queue.pop(0)

            if self.revise(var, con):
                if len(var.domain) == 0:
                    return False

                for x in list(set(self.neighbors(var)) - set(con)):
                    self.queue.append((x, var))

    def neighbors(self, Xi):
        return ['wat']

    def rerun(self):
        pass

    def revise(self, var, con):
        revised = False
        for x in var.domain:
            for y in con.domain:
                if x != y and con.method([x,y]):
                    self.csp.prune(var, x, self.removals)
                    revised = True
        return revised

    '''
    def revise(csp, Xi, Xj, removals):
    "Return true if we remove a value."
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every(lambda y: not csp.constraints(Xi, x, Xj, y),
                 csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised
    
    
    
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
    '''


def get_graph():
    input_graph = input("Select graph (1-6): ")
    input_graph = "graph" + str(input_graph) + ".txt"
    graph = open('modul2/' + input_graph, 'r').read().splitlines()
    return graph


def create_nodes(num_vertices, graph):
    nodes = []
    for i in range(1, num_vertices + 1):
        node = Node(i)
        state = [i for i in graph[i].split()]
        node.index = state[0]
        node.xPos = state[1]
        node.yPos = state[2]
        nodes.append(node)
    return nodes

#GAC -> memoize(lambda n: n[0]!=n[1])
#constraint = Constraint(i, GAC.method)


def set_constraints(num_vertices, graph):
    constraints = []
    for i in range(num_vertices + 1, len(graph)):
        constraint = Constraint([int(i) for i in graph[i].split()])
        constraints.append(constraint)
    return constraints


def get_vc_domain(k):
    variable_colors = ['red', 'green', 'blue', 'yellow', 'pink', 'brown', 'purple', 'orange']
    return variable_colors[0:k]


def init_problem():
    k = int(input("K-value (3-10): "))
    graph = get_graph()
    num_vertices = int([i for i in graph[0].split()][0])
    num_edges = int([i for i in graph[0].split()][1])

    nodes = create_nodes(num_vertices, graph)
    constraint = memoize(lambda n: n[0]!=n[1])
    constraints = set_constraints(num_vertices, graph)
    vc_dom = range(0,k)
    domains = {}
    for node in nodes:
        domains[node] = vc_dom


    csp = CSP(nodes, domains, constraints)
    gac = GAC(csp)
    gac.initialization()

    root = Tk()
    app = Gui(csp, master=root)
    app.mainloop()


if __name__ == '__main__':
    init_problem()


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
