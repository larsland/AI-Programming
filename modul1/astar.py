from tkinter import *
from heapq import heappush, heappop
from heapq import heappush, heappop
from math import sqrt, fabs
from itertools import count


class Astar_program(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master.title("A* Search")
        self.pack()
        self.canvas = Canvas(self, width=500, height=500)
        self.create_gui()

    def create_gui(self):

        # Variable for the current mode, and setting a default
        selected_mode = StringVar(self)
        selected_mode.set("Best-first mode")

        # Variable for the current map, and setting a default
        self.selected_map = StringVar(self)
        self.selected_map.set("map1.txt")

        # Creating the menus and buttons
        mode_menu = OptionMenu(self, selected_mode, "Best-first mode", "Depth-first mode", "Breadth-first mode", command = lambda mode:print(mode))
        map_menu = OptionMenu(self, self.selected_map, "map1.txt", "map2.txt", "map3.txt", "map4.txt", "map5.txt", "map6.txt", command = lambda map:self.create_grid(map))
        start_btn = Button(self, text="Start", fg="green", command = self.start_program)
        exit_btn = Button(self, text="Exit", fg="red", command = self.quit)

        # Placing components in a grid
        mode_menu.grid(row = 0, column = 0)
        map_menu.grid(row = 0, column = 1)
        start_btn.grid(row = 0, column = 2)
        exit_btn.grid(row = 0, column = 3)
        self.canvas.grid(row = 1, column = 0, columnspan = 4)

        self.create_grid(self.selected_map.get())

    def create_grid(self, board_matrix):
        map_string = ""

        if ".txt" in board_matrix:
            fo = open(board_matrix, "r")
            for line in fo.readlines():
                for c in line:
                    map_string += c

        x0_counter = 0
        y0_counter = 0
        x1_counter = 50
        y1_counter = 50

        for c in map_string:
            if c == '.':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="white")
            elif c == '#':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="black")
            elif c == 'A':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="green")
            elif c == 'B':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="red")
            elif c == 'x':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="yellow")


            x0_counter += 50
            x1_counter += 50

            if c == '\n':
                x0_counter = 0
                y0_counter += 50
                x1_counter = 50
                y1_counter += 50

    # Method for starting the application with the chosen algorithm
    def start_program(self):
        print ("START")

        '''
        b = Board(list(G))
        b.solve(a_star)
        # b.pretty_print()

        b = Board(list(G))
        b.solve(depth_first_search)
        # b.pretty_print()

        b = Board(list(G))
        b.solve(breadth_first_search)
        # b.pretty_print()
        '''







class Node:
    def __init__(self, state, problem, parent=None, action=None, path_cost=0):
        self.state = state
        self.problem = problem
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash("" + self.state)


class Board(Problem):
    def __init__(self, board):
        self.board = board  # Holds the input board for reference

        self.state = []  # Matrix of board Nodes
        self.open = []  # List of open Nodes
        self.closed = []  # List of closed Nodes

        self.goal = None  # The goal Node
        self.initial = None  # The initial Node

        self.counter = count()  # Unique sequence count for correct priority queue implementation

        # Sizes defining the board
        self.width = 0
        self.height = 0

        # Holds several solution related data instances
        self.solution = {'path': [], 'length': 0, 'found': False, 'steps': 0, 'states': []}

        self.init_state()  # Initialize state

        Problem.__init__(self, self.state, self.initial, self.goal)

    def __repr__(self):
        representation = '<Board ([\n'
        for line in list(self.board):
            representation += line+'\n'
        representation += '], \n'

        representation += 'initial node:  ' + str(self.initial) + '\n'
        representation += 'goal node:     ' + str(self.goal) + '\n)'
        representation += 'open:          ' + str(self.open) + '\n'
        representation += 'closed:        ' + str(self.closed) + '\n'
        representation += 'counter:       ' + str(next(self.counter)) + '\n'
        representation += 'solution path: ' + str(self.solution_path) + '\n'

        return representation

    def init_state(self):
        self.height = len(self.board)-1
        self.width = max(map(len, self.board))-1

        y = -1
        for row in list(self.board):
            node_row = []
            y += 1
            x = -1
            for tile in row:
                x += 1
                if tile != '\n':
                    node = PriorityNode(x, y, self, tile)

                    if tile == 'B':
                        # Goal node is set
                        self.goal = node
                    elif tile == 'A':
                        # Start node is opened
                        self.initial = node
                        self.open.append(node)
                    elif tile == '#':
                        # Walls are closed
                        node.closed = True
                        # self.closed.append(node)

                    node_row.append(node)
            self.state.append(node_row)

    # In our problem, actions are all nodes reachable from current Node within the board matrix
    def actions(self, node):
        try:
            if node.y > 0:  # UP
                child = self.state[node.y-1][node.x]
                if not child.closed:
                    yield child
            if node.y < self.height:  # DOWN
                child = self.state[node.y+1][node.x]
                if not child.closed:
                    yield child
            if node.x > 0:  # LEFT
                child = self.state[node.y][node.x-1]
                if not child.closed:
                    yield child
            if node.x < self.width:  # RIGHT
                child = self.state[node.y][node.x+1]
                if not child.closed:
                    yield child
        except IndexError as e:
            print(e)

    def save_state(self):
        self.solution['states'].append(self.state)

    def add_path(self, path, node):
        path_line = list(path[node.y])
        path_line[node.x] = 'x'
        path[node.y] = "".join(path_line)

        return path

    def solve(self, algorithm):
        path = list(self.board)

        solution_path, steps, found = algorithm(self)

        for node in solution_path:
            path = self.add_path(path, node)

        self.solution['path'] = path
        self.solution['length'] = len(solution_path)
        self.solution['steps'] = steps
        self.solution['found'] = path

    def solution_states_generator(self):
        for state in self.solution['states']:
            yield state

    def pretty_print(self):
        if self.solution['found']:
            print("Solution found in %s steps, solution length is %s" % (self.solution['steps'], self.solution['length']))
        else:
            print("No solution found in %s steps, solution length is %s" % (self.solution['steps'], float('inf')))

        print('_'*len(self.board[0]))
        for solution_line in self.solution['path']:
            print(solution_line)
        print('_'*len(self.board[0]))
        print('')


class Problem():
    def __init__(self, state, initial, goal=None, ):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.state = state
        self.initial = initial
        self.goal = goal

    def init_state(self):
        """Initialization method for the state of the problem,
        can be a list, matrix, tree or any other data structure that fits the problem"""
        pass

    def actions(self, state):
        """Returns all actions that can be performed from current state,
        either as a data structure or a generator"""
        pass

    def solve(self, algorithm):
        """Solve the problem with the given algorithm"""
        pass

    def goal_test(self, other):
        return self.goal == other

    def save_state(self):
        pass


class PriorityNode(Node):
    # Constructor
    def __init__(self, x, y, board, tile):
        # Coordinates
        self.x = x
        self.y = y

        self.tile = tile
        # Reference to the board class
        self.board = board

        # g and f scores
        self.g = 0
        self.f = 0

        # Heuristic function
        self.h = lambda x, y: sqrt((self.x-x)**2 + (self.y-y)**2)
        # self.h = lambda x, y: fabs(x-self.x) + fabs(y-self.y)

        # Priority Queue counter in case equal priority (f)
        self.c = 0

        self.closed = False

        Node.__init__(self, (x, y), board)

    def update_priority(self, goal, c):
        self.c = c
        self.f = self.g + self.h(goal.x, goal.y) * 10  # A*

    def __lt__(self, other):  # comparison method for priority queue
        return self.f + self.c < other.f + self.c

    def __repr__(self):
        return "<Node (x:%s, y:%s, f:%s, c:%s, t:%s)>" % (self.x, self.y, self.f, self.c, self.tile)




class PriorityQueue:
    def __init__(self):
        pass

    def add(self, problem, item):
        # Simulated memoization of f(n) = g(n) + h(n)
        if item.f:
            return
        item.update_priority(problem.goal, next(problem.counter))
        heappush(problem.open, item)

    def pop(self, queue):
        return heappop(queue)


class Stack:
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.append(item)

    def pop(self, stack):
        return stack.pop()


class FIFOQueue:
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.append(item)

    def pop(self, queue):
        return queue.pop(0)


def graph_search(problem, frontier):
    path, steps = [], 0
    while problem.open:
        node = frontier.pop(problem.open)
        steps += 1

        if node.closed:
            continue

        path.append(node)
        problem.save_state()

        if problem.goal_test(node):
            return path, steps, True

        for child_node in problem.actions(node):
            if child_node.closed:
                continue

            child_node.parent = node
            frontier.add(problem, child_node)

        # We have explored all the child nodes of this node, so we close it.
        node.closed = True
        # self.closed.append(node)

    return path, steps, False


def a_star(problem):
    return graph_search(problem, PriorityQueue())


def depth_first_search(problem):
    return graph_search(problem, Stack())


def breadth_first_search(problem):
    return graph_search(problem, FIFOQueue())


def main():
    root = Tk()
    app = Astar_program(master=root)
    app.mainloop()

main()







