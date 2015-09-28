from modul2.gui import Gui
from tkinter import *

class Node:
    def __init__(self, index):
        self.index = index
        self.xPos = 0.0
        self.yPos = 0.0
        self.domain = []
        self.color = "black"

    def __repr__(self):
        return "ID:"   + str(self.index) + \
            " Xpos:"   + str(self.xPos) + \
            " Ypos:"   + str(self.yPos) + \
            " Color:"  + str(self.color) + \
            " Domain:" + str(self.domain)


class CSP:
    def __init__(self, nodes, domain, constraints):
        self.nodes = nodes
        self.domain = domain
        self.constraints = constraints
        self.set_node_domains()

    def set_node_domains(self):
        for node in self.nodes:
            node.domain = self.domain

    def __repr__(self):
        return "Nodes: " + str(self.nodes) + '\n' + "Domain: " + str(self.domain) + '\n' + \
               "Constraints: " + str(self.constraints)


class GAC:
    def __init__(self, csp):
        self.csp = csp
        self.queue = []
        self.removals = []

    def initialization(self):
        for constraint in self.csp.constraints:
            self.queue.append((self.csp.nodes[int(constraint[0])], constraint))
            self.queue.append((self.csp.nodes[int(constraint[1])], constraint))
        print(self.queue)

    def domain_filtering(self):
        while self.queue:
            (var, con) = self.queue.pop(0)

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


def set_domain(k):
    variable_colors = ['red', 'green', 'blue', 'yellow', 'pink', 'brown']
    return variable_colors[0:k]


def init_problem():
    k = int(input("K-value: "))
    graph = get_graph()
    num_vertices = int([i for i in graph[0].split()][0])
    num_edges = int([i for i in graph[0].split()][1])

    nodes = create_nodes(num_vertices, graph)
    constraints = set_constraints(num_vertices, graph)
    domain = set_domain(k)

    csp = CSP(nodes, domain, constraints)
    gac = GAC(csp)
    gac.initialization()
    gac.domain_filtering()

    root = Tk()
    app = Gui(csp, master=root)
    app.mainloop()


if __name__ == '__main__':
    init_problem()








