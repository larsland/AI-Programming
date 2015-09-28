from modul2.gui import Gui
from tkinter import *
from algorithms.search import Problem

class Node:
    def __init__(self, index):
        self.index = index
        self.xPos = 0.0
        self.yPos = 0.0
        self.domain = []
        self.color = "black"

    def __repr__(self):
        return "ID:" + str(self.index)


class CSP(Problem):
    def __init__(self, nodes, domain, constraints):
        self.nodes = nodes
        self.domain = domain
        self.constraints = constraints

        Problem.__init__(self, (nodes, domain, constraints), (nodes, domain, constraints))

    def __repr__(self):
        return "Nodes: " + str(self.nodes) + '\n' + "Domain: " + str(self.domain) + '\n' + \
               "Constraints: " + str(self.constraints)

    def prune(self, var, value, removals):
        # Rule out var=value.
        self.domain[var].remove(value)
        if removals is not None:
            removals.append((var, value))


class GAC:
    def __init__(self, csp):
        self.csp = csp
        self.queue = []
        self.removals = []

    def initialization(self):
        for constraint in self.csp.constraints:
            for var in constraint:
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
            # if no value y in Dj allows (x,y) to satisfy the constraint between Xi and Xj:
            if x not in [c.domain for c in con]:
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
    '''


def get_graph():
    input_graph = input("Select graph (1-6): ")
    input_graph = "graph" + input_graph + ".txt"
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


def set_constraints(num_vertices, graph):
    constraints = []
    for i in range(num_vertices + 1, len(graph)):
        constraint = [int(i) for i in graph[i].split()]
        constraints.append(constraint)
    return constraints


def get_vc_domain(k):
    variable_colors = ['red', 'green', 'blue', 'yellow', 'pink', 'brown']
    return variable_colors[0:k]


def init_problem():
    k = int(input("K-value: "))
    graph = get_graph()
    num_vertices = int([i for i in graph[0].split()][0])
    num_edges = int([i for i in graph[0].split()][1])

    nodes = create_nodes(num_vertices, graph)
    constraints = set_constraints(num_vertices, graph)
    vc_dom = get_vc_domain(k)
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








