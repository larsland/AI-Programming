class Node:
    def __init__(self, index):
        self.index = index
        self.domain = []
        self.xPos = 0.0
        self.yPos = 0.0

    def __repr__(self):
        return "ID:" + str(self.index) +" Xpos:" + str(self.xPos) + " Ypos" + str(self.yPos)

class CSP:
    def __init__(self, vars, k):
        self.k = k
        self.vars = vars

    def __repr__(self):
        return "Nodes: " + str(self.vars) + "K-value: " + str(self.k)



def get_graph():
    graph = open('modul2/graph.txt', 'r').read().splitlines()
    k = int(input("K-value: "))
    num_vertices = int(graph[0][0])
    num_edges = graph[0][2]

    nodes = []

    for i in range(1, num_vertices + 1):
        node = Node(i)
        node.index = graph[i][0]
        node.xPos = graph[i][1:5]
        node.yPos = graph[i][5::]
        nodes.append(node)

    csp = CSP(nodes, k)
    print(csp)


if __name__ == '__main__':
    get_graph()








