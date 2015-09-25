class Node:
    def __init__(self, index):
        self.index = index
        self.domain = []
        self.xPos = 0.0
        self.yPos = 0.0

    def __repr__(self):
        return "ID:" + str(self.index) +" Xpos:" + str(self.xPos) + " Ypos:" + str(self.yPos)


class CSP:
    def __init__(self, nodes, k):
        self.k = k
        self.nodes = nodes
        self.domain = self.set_domain()

    def __repr__(self):
        return "Nodes: " + str(self.nodes) + "K-value: " + str(self.k)

    def set_domain(self):
        variable_colors = ['red', 'green', 'blue', 'yellow', 'pink', 'brown']
        return variable_colors[0:self.k]


def get_graph():
    input_graph = input("Select graph (1-6): ")
    k = int(input("K-value: "))

    input_graph = "graph" + input_graph + ".txt"
    graph = open('modul2/' + input_graph, 'r').read().splitlines()

    num_vertices = int([i for i in graph[0].split()][0])
    num_edges = int([i for i in graph[0].split()][1])

    nodes = []

    for i in range(1, num_vertices + 1):
        node = Node(i)
        state = [i for i in graph[i].split()]
        node.index = state[0]
        node.xPos = state[1]
        node.yPos = state[2]
        nodes.append(node)

    csp = CSP(nodes, k)
    print(csp)


if __name__ == '__main__':
    get_graph()








