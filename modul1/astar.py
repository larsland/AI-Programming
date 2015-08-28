from tkinter import *
from heapq import heappush, heappop
from collections import deque
from math import sqrt, fabs, floor, ceil
from itertools import count
import time


class Astar_program(Frame):

    def __init__(self, master=None):
        self.selected_mode = None
        self.selected_map = None
        self.solutions = None
        self.step = 0
        Frame.__init__(self, master)
        self.master.title("A* Search")
        self.pack()
        self.canvas = Canvas(self, width=200, height=0)
        self.create_gui()

        # 64 length green to yellow to red gradient
        self.heat_gradient = ['#79FE48', '#7EFE47', '#83FE47', '#88FE46', '#8DFE46', '#92FE45', '#96FE45', '#9BFE44',
                              '#A0FE44', '#A5FE43', '#AAFE43', '#AFFE42', '#B4FE42', '#BAFE41', '#BFFE41', '#C4FE40',
                              '#C9FE40', '#CEFE3F', '#D3FE3F', '#D9FE3E', '#DEFE3E', '#E3FE3D', '#E9FE3D', '#EEFE3C',
                              '#F3FE3C', '#F9FE3B', '#FEFD3B', '#FEF83A', '#FEF33A', '#FEED39', '#FEE739', '#FEE238',
                              '#FEDC38', '#FED737', '#FED137', '#FECB36', '#FEC636', '#FEC035', '#FEBA35', '#FEB434',
                              '#FEAE34', '#FEA933', '#FEA333', '#FE9D32', '#FE9732', '#FE9131', '#FE8B31', '#FE8530',
                              '#FE7F30', '#FE792F', '#FE732F', '#FE6C2E', '#FE662E', '#FE602D', '#FE5A2D', '#FE542C',
                              '#FE4D2C', '#FE472B', '#FE412B', '#FE3A2A', '#FE342A', '#FE2D29', '#FE292B', '#FF2830']

        global cancel_animation_id
        cancel_animation_id = None

    def create_gui(self):
        # Initiating string variables to bind to various GUI components
        self.selected_mode = StringVar(self)
        self.selected_map = StringVar(self)
        self.map_data = StringVar(self)

        # Setting default values
        self.selected_mode.set("A*")
        self.selected_map.set("map1.txt")

        # Creating the menus and buttons
        mode_menu = OptionMenu(self, self.selected_mode, "A*", "Breadth-first", "Depth-first",
                               command=lambda: self.reset_grid())
        map_menu = OptionMenu(self, self.selected_map, "map1.txt", "map2.txt", "map3.txt", "map4.txt", "map5.txt",
                              command=lambda matrix: self.reset_grid(matrix))
        start_btn = Button(self, text="Solve", fg="green", command=self.start_program)
        exit_btn = Button(self, text="Exit", fg="red", command=self.quit)
        next_step_btn = Button(self, text="Next", fg="green", command=self.next_solution_grid)
        prev_step_btn = Button(self, text="Back", fg="red", command=self.prev_solution_grid)
        self.custom_map_field = Text(self, width = 20, height = 10)
        load_custom_map_btn = Button(self, text="Check map info", command = self.load_custom_map)

        # Placing components in a grid
        mode_menu.grid(row=0, column=0)
        map_menu.grid(row=0, column=1)
        start_btn.grid(row=0, column=2)
        prev_step_btn.grid(row=0, column=3)
        next_step_btn.grid(row=0, column=4)
        exit_btn.grid(row=0, column=5)
        self.canvas.grid(row=1, column=0, columnspan=6)
        load_custom_map_btn.grid(row=0, column=6)
        self.custom_map_field.grid(row=1, column=6)

        # Calls the method which creates the GUI grid based on the default map
        self.create_grid(self.selected_map.get())

    def create_grid(self, board_matrix):
        map_string = ""
        y_counter = 0

        # Checking if the board comes from a file, or as a path
        if ".txt" in board_matrix:
            fo = open(board_matrix, "r")
            for line in fo.readlines():
                y_counter += 1
                for c in line:
                    map_string += c
        else:
            for c in board_matrix:
                y_counter += 1
                map_string += c

        # Changing the size of the canvas according to the current map dimensions
        print(len(map_string))
        self.canvas.config(width=len(map_string), height=len(map_string))

        x0_counter = 0
        y0_counter = 0
        x1_counter = 30
        y1_counter = 30

        for c in map_string:
            if c == '.':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="white")
            elif c == '#':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="#121f1f")
            elif c == 'A':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="green")
            elif c == 'B':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="red")
            elif c == 'x':
                self.canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="yellow")

            x0_counter += 30
            x1_counter += 30

            if c == '\n':
                x0_counter = 0
                y0_counter += 30
                x1_counter = 30
                y1_counter += 30

    def load_custom_map(self):
        input = self.custom_map_field.get("1.0", 'end-1c').split('\n')

        data = {'size':input[0], 'start':input[1], 'goal':input[2], 'blockade':input[3::]}

        size_x = int(data['size'][0:data['size'].index(',')])
        size_y = int(data['size'][data['size'].index(',')+1::])

        start_x = int(data['start'][0:data['start'].index(',')])
        start_y = int(data['start'][data['start'].index(',')+1::])

        goal_x = int(data['goal'][0:data['goal'].index(',')])
        goal_y = int(data['goal'][data['goal'].index(',')+1::])

        matrix = [['.' for ni in range(size_x)] for mi in range(size_y)]
        matrix[start_x][start_y] = 'A'
        matrix[goal_x][goal_y] = 'B'

        for line in reversed(matrix):
            print(line)


    def next_solution_grid(self):
        self.step += 1
        self.create_solution_grid(self.solutions[self.step])

    def prev_solution_grid(self):
        self.step += 1
        self.create_solution_grid(self.solutions[self.step])

    def create_solution_grid(self, solution):
        matrix = solution['state']
        #    max_f = max(node_list, key=lambda n: n.f)
        min_f = min([min(node_list, key=lambda n: n.f) for node_list in matrix], key=lambda n: n.f).f or 0
        max_f = max([max(node_list, key=lambda n: n.f) for node_list in matrix], key=lambda n: n.f).f or 1
        max_f -= min_f

        open_nodes = solution['open']
        self.canvas.config(width=len(matrix)*30, height=len(matrix[0])*30)
        for node_list in matrix:
            for node in node_list:
                if node.tile == '#':
                    self.canvas.create_rectangle(node.x*30, node.y*30, (node.x+1)*30, (node.y+1)*30, fill="#121f1f")
                elif node.tile == 'B':
                    self.canvas.create_rectangle(node.x*30, node.y*30, (node.x+1)*30, (node.y+1)*30, fill="red")
                elif node.tile == 'A':
                    self.canvas.create_rectangle(node.x*30, node.y*30, (node.x+1)*30, (node.y+1)*30, fill="green")
                elif node.closed:
                    weight = float(node.f)
                    heat_length = float(len(self.heat_gradient))
                    if weight == 0 or weight is None:
                        pos = 0
                    else:
                        pos = floor(heat_length - ((heat_length / max_f) * weight))
                    color = self.heat_gradient[pos]
                    self.canvas.create_rectangle(node.x*30, node.y*30, (node.x+1)*30, (node.y+1)*30, fill=color)
                elif node in open_nodes:
                    self.canvas.create_rectangle(node.x*30, node.y*30, (node.x+1)*30, (node.y+1)*30, fill="#add8e6")

    def update_solution_animation(self, label, ani_step, ms_delay, frame_num):
        global cancel_animation_id
        if frame_num == len(ani_step) - 1:
            self.cancel_animation()
            return

        self.create_solution_grid(ani_step[frame_num])
        frame_num = (frame_num + 1) % len(ani_step)
        print("update_solution_animation", (frame_num + 1, len(ani_step)))
        cancel_animation_id = self.after(
            ms_delay, self.update_solution_animation, label, ani_step, ms_delay, frame_num)

    def begin_solution_animation(self):
        print("begin_solution")
        global cancel_animation_id
        self.cancel_animation()
        self.reset_grid()
        ms_delay = floor(1000 / float(len(self.solutions)))
        print(ms_delay)
        cancel_animation_id = self.after(
            ms_delay, self.update_solution_animation, None, self.solutions, ms_delay, 0)

    def cancel_animation(self):
        global cancel_animation_id
        if cancel_animation_id is not None:
            self.after_cancel(cancel_animation_id)
            cancel_animation_id = None

    def reset_grid(self, matrix=None):
        self.canvas.delete("all")
        self.create_grid(matrix or self.selected_map.get())

    # Method for starting the application with the chosen algorithm
    def start_program(self):
        b = Board(list(open(self.selected_map.get()).readlines()))

        if self.selected_mode.get() == "A*":
            b.solve(a_star)
        elif self.selected_mode.get() == "Breadth-first":
            b.solve(breadth_first_search)
        elif self.selected_mode.get() == "Depth-first":
            b.solve(depth_first_search)

        b.pretty_print()

        self.solutions = b.solution['states']

        self.begin_solution_animation()


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


class Problem():
    def __init__(self, state, initial, goal=None):
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
        """General goal test to see if goal has been achieved"""
        return self.goal == other

    def save_state(self):
        """Useful when you want to review the states your algorithm created"""
        pass


class PriorityNode(Node):
    """This node is specialized to be used in the context of a priority heap (or queue).
    The order of nodes is derived from the comparison method __lt__, based on priority, as seen below.
    For the purpose of this task the priority is calculated from f(n) = g(n) + h(n).
    """

    def __init__(self, node_x, node_y, board, tile):
        # Coordinates
        self.x = node_x
        self.y = node_y

        self.tile = tile    # 'A', 'B', '.' or '#'
        self.board = board  # Reference to the board class

        # g and f scores
        self.g = 0
        self.f = 0

        # Heuristic function with euclidean distance.
        self.h = lambda x, y: sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        # Heuristic function with manhattan distance.
        # self.h = lambda x, y: fabs(x-self.x) + fabs(y-self.y)

        self.c = 0              # Priority Queue counter in case equal priority (f)
        self.closed = False     # Use this to check if the node has been traversed.

        Node.__init__(self, (node_x, node_y), board)

    def update_priority(self, goal, c):
        self.c = c
        self.f = self.g + self.h(goal.x, goal.y) * 10  # A*

    def __lt__(self, other):
        """Comparison method for priority queue"""
        return self.f + self.c < other.f + self.c

    def __repr__(self):
        """Representation method for printing a Node with valuable information"""
        return "<Node (x:%s, y:%s, f:%s, c:%s, t:%s)>" % (self.x, self.y, self.f, self.c, self.tile)


class Board(Problem):
    """The problem in this task is a matrix of nodes, which can be thought of as a board.
    This board problem contains the variables needed to represent this matrix, and the
    methods needed to allow an algorithm to solve it. This includes the problem
    initialization and the generation of possible actions for the current state."""

    def __init__(self, board):
        self.board = board      # Holds the input board for reference
        self.state = []         # Matrix of board Nodes
        self.open = []          # List of open Nodes
        self.goal = None        # The goal Node
        self.initial = None     # The initial Node
        self.counter = count()  # Unique sequence count for correct action priority

        # Sizes defining the board
        self.width = 0
        self.height = 0

        # Holds several solution related data instances
        self.solution = {'path': [], 'length': 0, 'found': False, 'steps': 0, 'states': []}

        # Initialize super class
        Problem.__init__(self, self.state, self.initial, self.goal)

    def __repr__(self):
        """Representation method for printing a Board with valuable information"""
        representation = '<Board ([\n'
        for line in list(self.board):
            representation += line + '\n'
        representation += '], \n'

        representation += 'initial node:  ' + str(self.initial) + '\n'
        representation += 'goal node:     ' + str(self.goal) + '\n)'
        representation += 'open:          ' + str(self.open) + '\n'
        representation += 'counter:       ' + str(next(self.counter)) + '\n'
        representation += 'solution path: ' + str(self.solution['path']) + '\n'

        return representation

    def init_state(self):
        """Initialize the problem state by feeding the problem through a set of rules """
        self.height = len(self.board) - 1                   # Get the height and width of the problem
        self.width = max(map(len, self.board)) - 1

        y = -1
        for row in list(self.board):                        # For each row in the board
            node_row = []
            y += 1
            x = -1
            for tile in row:                                # For each tile in the board row
                x += 1
                if tile != '\n':                            # If tile not a line break then
                    node = PriorityNode(x, y, self, tile)   # create the PriorityNode based on position and tile value.

                    if tile == 'B':                         # If tile has value of B then
                        self.goal = node                    # set this node as the goal node.
                    elif tile == 'A':                       # If tile has value of A then
                        self.initial = node                 # set this node as start node and
                        self.open.append(node)              # add it to the open set.
                    elif tile == '#':                       # If tile has value of # then
                        node.closed = True                  # close the node as it can not be accessed.

                    node_row.append(node)                   # Add node to current row of nodes and
            self.state.append(node_row)                     # add row of nodes to the problem state.

    def actions(self, node):
        """In our problem, actions are all nodes reachable from current Node within the board matrix"""
        try:
            if node.y > 0:
                yield self.state[node.y - 1][node.x]    # Up
            if node.y < self.height:
                yield self.state[node.y + 1][node.x]    # Down
            if node.x > 0:
                yield self.state[node.y][node.x - 1]    # Left
            if node.x < self.width:
                yield self.state[node.y][node.x + 1]    # Right
        except IndexError:
            pass

    def add_path(self, path, node):
        path_line = list(path[node.y])
        path_line[node.x] = 'x'
        path[node.y] = "".join(path_line)

        return path

    def solve(self, algorithm):

        """Problem solver that takes in a selected algorithm and
        formats the response in a handy way via our solution dictionary"""
        path = list(self.board)

        solution_path, steps, found = algorithm(self)

        for node in solution_path:
            path = self.add_path(path, node)

        self.solution['path'] = path
        self.solution['length'] = len(solution_path)
        self.solution['steps'] = steps
        self.solution['found'] = path

    def save_state(self):
        """For storing states as the algorithm traverses the problem"""

        state = {'state': list(self.state), 'open': list(self.open), 'path': list(self.board)}
        self.solution['states'].append(state)

    def solution_states_generator(self):
        """Generator for all the solution states"""
        solutions = self.solution['states']
        for state in solutions:
            yield state

    def pretty_print(self):
        """Helper method for beautiful printing of the problem solution"""
        if self.solution['found']:
            print(
                "Solution found in %s steps, solution length is %s" % (self.solution['steps'], self.solution['length']))
        else:
            print("No solution found in %s steps, solution length is %s" % (self.solution['steps'], float('inf')))

        print('_' * len(self.board[0]))
        for solution_line in self.solution['path']:
            print(solution_line)
        print('_' * len(self.board[0]))
        print('')


class PriorityQueue:
    def __init__(self):
        pass

    def add(self, problem, node):
        # Simulated memoization of f(n) = g(n) + h(n)
        if node.f:
            return

        # Update the priority of the node based on its proximity to the goal
        # as well as a tie-breaker in the form of a counter.
        node.update_priority(problem.goal, next(problem.counter))
        # Push node onto heap
        heappush(problem.open, node)

    def pop(self, queue):
        # Use heappop to retrieve node with highest priority
        return heappop(queue)


class LIFOQueue:
    # Also known as a Stack
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.appendleft(item)  # First in

    def pop(self, queue):
        return queue.popleft()  # Last out


class FIFOQueue:
    def __init__(self):
        pass

    def add(self, problem, item):
        problem.open.appendleft(item)  # First in

    def pop(self, queue):
        return queue.pop()  # First out


def graph_search(problem, frontier):
    """ A normal Graph search contains all the necessary tools to implement the three algorithms
     specified in the task."""
    problem.init_state()                            # Initialize problem state
    path, steps = [], 0                             # Containers for path and amount of steps taken
    while problem.open:                             # While there are still nodes in the queue
        node = frontier.pop(problem.open)           # Pop node
        steps += 1                                  # Increment steps taken

        if node.closed:                             # If node has been closed then
            continue                                # skip to next iteration

        path.append(node)                           # Save path and
        problem.save_state()                        # current state

        if problem.goal_test(node):                 # Is current node the goal node? Then
            return path, steps, True                # end algorithm and return result

        for child_node in problem.actions(node):    # For each child node reachable from the current node,
            if child_node.closed:                   # if child node has been closed then
                continue                            # skip to next iteration

            frontier.add(problem, child_node)       # Add child to list of open nodes

        node.closed = True                          # All the child nodes of this node have been explored so we close it
        # Alternative: self.closed.append(node)

    return path, steps, False                       # End algorithm and return result


def a_star(problem):
    """A* is a graph search with a heuristic.
    In our implementation we use our Priority Nodes
    with their heuristic as well as a PriorityQueue
    to implement the A* algorithm."""
    return graph_search(problem, PriorityQueue())


def depth_first_search(problem):
    """Depth first search is a graph search
    where the open nodes are on a Last In First Out queue (LIFO),
    also known as a Stack"""
    problem.open = deque()
    return graph_search(problem, LIFOQueue())


def breadth_first_search(problem):
    """Depth first search is a graph search
    where the open nodes are on a First In first Out queue (LIFO)"""
    problem.open = deque()
    return graph_search(problem, FIFOQueue())


def main():
    root = Tk()
    app = Astar_program(master=root)
    app.mainloop()

main()







