from tkinter import *
from heapq import heappush, heappop
from functools import wraps
from random import randrange
from pprint import pprint
from math import sqrt, fabs
import itertools
import time


class Astar_program(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master.title("A* Search")
        self.pack()

        self.board = Board()
        self.selected_map = "map1.txt"

        # Creating the canvas where the grid is drawn
        self.canvas = Canvas(self, width=500, height=500)
        self.create_gui()

    def create_gui(self):

        # Variable for the current mode, and setting a default
        selected_mode = StringVar(self)
        selected_mode.set("Best-first mode")

        # Variable for the current map, and setting a default
        self.selected_map = StringVar(self)
        self.selected_map.set('map1.txt')

        # Creating the menus and buttons
        mode_menu = OptionMenu(self, selected_mode, "Best-first mode", "Depth-first mode", "Breadth-first mode",
                               command=lambda mode:print(mode))
        map_menu = OptionMenu(self, self.selected_map, "map1.txt", "map2.txt", "map3.txt", "map4.txt", "map5.txt",
                              "map6.txt", command=self.create_grid)
        start_btn = Button(self, text="Start", fg="green", command=self.start_program)
        exit_btn = Button(self, text="Exit", fg="red", command=self.quit)

        # Placing components in a grid
        mode_menu.grid(row = 0, column = 0)
        map_menu.grid(row = 0, column = 1)
        start_btn.grid(row = 0, column = 2)
        exit_btn.grid(row = 0, column = 3)
        self.canvas.grid(row = 1, column = 0, columnspan = 4)

        # Sending the default map to the method which created the graphical map
        #self.create_grid()

    def create_grid(self, board_map=None):
        map_string = ""
        board_matrix = open(board_map).readlines()

        for line in board_matrix:
            for c in line:
                map_string += c

        print(map_string)

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
        print("Running A-Star...")
        board_matrix = (open(self.selected_map.get()).readlines())

        self.board = Board()
        self.board.add_board(board_matrix)

        for line in self.board.solve():
            self.create_grid(line)


            

class Node:
    # Constructor
    def __init__(self, x, y, tile, board):
        # Coordinates
        self.x = x
        self.y = y

        self.tile = tile
        # Reference to the board class
        self.board = board

        # g and f scores
        self.g = 0
        self.h = lambda x, y: sqrt((self.x-x)**2 + (self.y-y)**2)
        # self.h = lambda x, y: fabs(x-self.x) + fabs(y-self.y)
        self.f = 0

        self.siblings = []

    def path(self):
        # Return a list of nodes forming the path from the root to this node.
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # Generates the valid siblings for the Node within the board matrix
    def get_siblings(self):
        # Init array for the parents
        siblings = []

        b_matrix = self.board.board_matrix
        height = len(b_matrix)-1
        width = len(b_matrix[0])-1

        try:
            # Remember that when using x and y as indexes, you must calculate with -1.
            if self.y > 0:
                # Up
                # print("UP", b_matrix[self.y-1][self.x])
                siblings.append(b_matrix[self.y-1][self.x])
            if self.y < height:
                # Down
                # print("DOWN", b_matrix[self.y+1][self.x])
                siblings.append(b_matrix[self.y+1][self.x])
            if self.x > 0:
                # Left
                # print("LEFT", b_matrix[self.y][self.x-1])
                siblings.append(b_matrix[self.y][self.x-1])
            if self.x < width:
                # Right
                # print("RIGHT", b_matrix[self.y][self.x+1])
                siblings.append(b_matrix[self.y][self.x+1])
        except IndexError as e:
            print (e)
            print (self)
            print (height)

        # Return list of siblings
        return siblings

    def update_priority(self, goal):
        self.f = self.g + self.h(goal.x, goal.y) * 10  # A*

    def __lt__(self, other):  # comparison method for priority queue
        return self.f < other.f

    def __repr__(self):
        return "<Node (%s, %s, %s)>" % (self.x, self.y, self.f)

    # May not need these
    def __eq__(self, other):
        return isinstance(other, Node) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash("" + self.x + self.y)


class Board:
    def __init__(self):
        self.input_rows = [] # Contains the input to add board
        self.board_matrix = []  # Contains the entire board
        self.open = []  # List of open Nodes
        self.closed = []  # List of closed Nodes
        self.goal = None  # The goal Node
        self.start = None

        # Sizes defining the board
        self.width = 0
        self.height = 0

    # Calculate manhattan score for a given Node
    # def manhattan_distance(self, node):
    #    return fabs(self.goal.x - node.x) + fabs(self.goal.y - node.y)

    def add_board(self, rows):
        self.input_rows = rows
        self.height = len(rows)-1
        self.width = len(max(rows, key=len))-1

        y = -1
        for row in rows:
            node_row = []
            y += 1
            x = -1
            for tile in row:
                x += 1
                if tile != '\n':
                    node = Node(x, y, tile, self)

                    if tile == 'B':
                        # Goal node is set
                        self.goal = node
                    elif tile == 'A':
                        # Start node is opened
                        self.start = node
                        heappush(self.open, node)
                    elif tile == '_':
                        # Normal nodes are added to open queue
                        heappush(self.open, node)
                    elif tile == '#':
                        # Walls are closed
                        self.closed.append(node)

                    node_row.append(node)
            self.board_matrix.append(node_row)

    def a_star(self):
        inf = float('inf')

        path = []
        while self.open:
            node = heappop(self.open)
            if node in self.closed:
                continue
            path.append(node)
            self.closed.append(node)
            if node == self.goal:
                return path, len(path), True

            for sibling in node.get_siblings():
                sibling.update_priority(self.goal)
                heappush(self.open, sibling)

        return path, len(path), False

    def add_path(self, path, node, i):
        path_line = list(path[node.y])
        path_line[node.x] = 'x'
        path[node.y] = "".join(path_line)

        print('-'*self.width + '-\n')
        for line in path:
            print (str(line))

        return path

    def solve(self):
        path = self.input_rows

        i = 0
        a_star_path, steps, found = self.a_star()
        if found:
            print("Solution found in %s steps" % steps)
        else:
            print("No solution found in %s steps" % steps)

        for node in a_star_path:
            i += 1
            yield self.add_path(path, node, i)


def main():
    root = Tk()
    app = Astar_program(master=root)
    app.mainloop()

main()











