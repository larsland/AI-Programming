from modul2.gui import Gui
from tkinter import *


class Node:
    def __init__(self, index):
        self.index = index
        self.xPos = 0.0
        self.yPos = 0.0
        self.color = "black"

    def __repr__(self):
        return "ID:" + str(self.index) + " Xpos:" + str(self.xPos) + " Ypos:" + str(self.yPos)


class CSP:
    def __init__(self, nodes, domain, constraints):
        self.nodes = nodes
        self.domain = domain
        self.constraints = constraints

    def __repr__(self):
        return "Nodes: " + str(self.nodes) + '\n' + "Domain: " + str(self.domain) + '\n' + \
               "Constraints: " + str(self.constraints)


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
        constraint = [i for i in graph[i].split()]
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

    root = Tk()
    app = Gui(csp, master=root)
    app.mainloop()


if __name__ == '__main__':
    init_problem()








