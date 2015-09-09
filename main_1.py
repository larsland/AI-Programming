from algorithms.search import a_star, breadth_first_search, depth_first_search
from modul1.problem import Board
from tkinter import *
import math


class Astar_program(Frame):
    def __init__(self, master=None):
        self.custom_map_field = None
        self.selected_mode = None
        self.selected_map = None
        self.solutions = []
        self.map_data = None
        self.board = None
        self.step = 0
        Frame.__init__(self, master)
        self.master.title("A* Search")
        self.pack()
        self.canvas = Canvas(self, width=0, height=0, highlightbackground='black', highlightthickness=1)
        self.cells = [[]]
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
                               command=self.reset_grid)
        map_menu = OptionMenu(self, self.selected_map, "map1.txt", "map2.txt", "map3.txt", "map4.txt", "map5.txt",
                              command=lambda matrix: self.reset_grid(matrix))
        start_btn = Button(self, text="Solve", fg="green", command=self.start_program)
        exit_btn = Button(self, text="Exit", fg="red", command=self.quit)
        next_step_btn = Button(self, text="Next", fg="green", command=self.next_solution_grid)
        prev_step_btn = Button(self, text="Back", fg="red", command=self.prev_solution_grid)
        self.custom_map_field = Text(self, width=20, height=10, highlightbackground='black', highlightthickness=1)
        load_custom_map_btn = Button(self, text="Load from text",
                                     command=self.load_custom_map)

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
        self.create_grid(self.selected_map.get(), is_file=True)

    def create_grid(self, matrix, is_file=False):
        for cell_row in self.cells:
            for cell in cell_row:
                self.canvas.delete(cell)

        if is_file:
            matrix = list(open('modul1/'+matrix).readlines())

        width = len(matrix)
        height = len(matrix[0])
        self.cells = [[None for _ in range(height)] for _ in range(width)]

        self.canvas.config(width=width*30, height=height*30)
        y = -1
        for line in matrix:
            x = -1
            y += 1
            for item in line:
                x += 1
                if type(item) is not str:
                    item, x, y = item.tile, item.x, item.y
                if item == '#':
                    self.cells[x][y] = self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill="#121f1f",
                                                                    tags='rectangle')
                elif item == '.':
                    self.cells[x][y] = self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill="white",
                                                                    tags='rectangle')
                elif item == 'B':
                    self.cells[x][y] = self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill="red",
                                                                    tags='rectangle')
                elif item == 'A':
                    self.cells[x][y] = self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill="green",
                                                                    tags='rectangle')

    def get_blocks(self, blockade):
        blocks = []
        x, y = blockade[0], blockade[1]
        blocks.append([x, y])
        for i in range(0, blockade[2]):
            for j in range(0, blockade[3]):
                blocks.append([x+i, y+j])
        return blocks

    def load_custom_map(self):
        try:
            _input = self.custom_map_field.get("1.0", 'end-1c').split('\n')

            intify = lambda items: [int(item) for item in items]

            size = intify(_input[0].split(','))
            start_node = intify(_input[1].split(','))
            goal_node = intify(_input[2].split(','))
            blockades = [intify(in_str.split(',')) for in_str in _input[3::]]

            matrix = [['.' for _ in range(size[0])] for _ in range(size[1])]
            for blockade in blockades:
                for block in self.get_blocks(blockade):
                    x, y = block[0], block[1]
                    if x < size[0] and y < size[1]:
                        matrix[block[0]][block[1]] = '#'


            matrix[start_node[0]][start_node[1]] = 'A'
            matrix[goal_node[0]][goal_node[1]] = 'B'

            self.board = matrix
            self.reset_grid(matrix)

        except Exception as e:
            print("no boi:", e)

    def next_solution_grid(self):
        if self.step < len(self.solutions):
            self.step += 1
            self.create_solution_grid(self.solutions[self.step-1])
        elif self.step == 0:
            self.start_program()

    def prev_solution_grid(self):
        print(self.step)
        if self.step > 0:
            self.step -= 1
            self.create_solution_grid(self.solutions[self.step-1])

    def create_solution_grid(self, solution):
        if type(solution) == str:
            self.create_grid(solution)
            return

        matrix = solution['state']
        min_f = min([min(node_list, key=lambda n: n.f) for node_list in matrix], key=lambda n: n.f).f or 0
        max_f = max([max(node_list, key=lambda n: n.f) for node_list in matrix], key=lambda n: n.f).f or 1
        max_f -= min_f

        open_nodes = solution['open']
        self.canvas.config(width=len(matrix)*30, height=(len(matrix[0])+1)*30)
        for node_list in matrix:
            for node in node_list:
                self.update_rectangle(node, open_nodes, max_f)

    def update_rectangle(self, node, open_nodes, max_f):
        if node.tile == '#':
            self.canvas.itemconfig(self.cells[node.x][node.y], fill='#121f1f')
        elif node.tile == 'B':
            self.canvas.itemconfig(self.cells[node.x][node.y], fill='red')
        elif node.tile == 'A':
            self.canvas.itemconfig(self.cells[node.x][node.y], fill='green')
        elif node in open_nodes:
            if self.canvas.gettags(self.cells[node.x][node.y]) != 'oval':
                self.canvas.delete(self.cells[node.x][node.y])
                self.cells[node.x][node.y] = self.canvas.create_oval(node.x*30, node.y*30, (node.x+1)*30, (node.y+1)*30,
                                                                     fill=self.get_heat_color(node, max_f),
                                                                     tags='oval')
        elif node.closed:
            if self.canvas.gettags(self.cells[node.x][node.y]) != 'rectangle':
                self.canvas.delete(self.cells[node.x][node.y])
                self.cells[node.x][node.y] = self.canvas.create_rectangle(
                    node.x*30, node.y*30, (node.x+1)*30, (node.y+1)*30,
                    fill=self.get_heat_color(node, max_f), tags='rectangle')

    def get_heat_color(self, node, max_f):
        weight = float(node.f)
        heat_length = float(len(self.heat_gradient))
        if weight == 0 or weight is None:
            pos = 0
        else:
            pos = math.floor(heat_length - ((heat_length / max_f) * weight))
        color = self.heat_gradient[pos]
        return color

    def begin_solution_animation(self):
        global cancel_animation_id
        self.reset_grid(self.board)
        ms_delay = math.floor(2000 / float(len(self.solutions)))
        print(ms_delay)
        cancel_animation_id = self.after(
            ms_delay, self.update_solution_animation, None, self.solutions, ms_delay, 0)

    def update_solution_animation(self, label, ani_step, ms_delay, frame_num):
        global cancel_animation_id
        if frame_num == len(ani_step):
            self.cancel_animation()
            return

        self.create_solution_grid(ani_step[frame_num])
        frame_num = (frame_num + 1) % (len(ani_step) + 1)
        cancel_animation_id = self.after(
            ms_delay, self.update_solution_animation, label, ani_step, ms_delay, frame_num)

    def cancel_animation(self):
        global cancel_animation_id
        if cancel_animation_id is not None:
            self.after_cancel(cancel_animation_id)
            cancel_animation_id = None
            return

    def reset_grid(self, matrix=None):
        self.cancel_animation()
        if matrix:
            self.create_grid(matrix)
        else:
            self.create_grid(self.selected_map.get(), is_file=True)

    # Method for starting the application with the chosen algorithm
    def start_program(self):
        if not self.board:
            self.board = list(open('modul1/'+self.selected_map.get()).readlines())
        board = Board(list(self.board))

        if self.selected_mode.get() == 'A*':
            board.solve(a_star)
        elif self.selected_mode.get() == 'Breadth-first':
            board.solve(breadth_first_search)
        elif self.selected_mode.get() == 'Depth-first':
            board.solve(depth_first_search)

        board.pretty_print()

        self.solutions = board.solution['states']
        self.step = board.solution['steps']
        self.begin_solution_animation()


def main():
    root = Tk()
    app = Astar_program(master=root)
    app.mainloop()

main()


"""
def create_grid_from_string(self, board_matrix):
    print(board_matrix)
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
"""







