from algorithms.old_search import a_star, breadth_first_search, depth_first_search
from modul1.board_problem import Board
from tkinter import *
import math


class Astar_program(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.problem = None
        self.custom_map_field = None
        self.selected_mode = None
        self.selected_map = None
        self.map_data = None
        self.board = None
        self.master.title("A* Search")
        self.pack()
        self.group_view = LabelFrame(self, text="View", padx=5, pady=5)
        self.canvas = Canvas(self.group_view, width=600, height=600, highlightbackground='black', highlightthickness=1)

        self.label_time = None
        self.label_steps = None
        self.label_open = None
        self.label_closed = None
        self.display_time = None
        self.display_steps = None
        self.display_open = None
        self.display_closed = None

        self.solutions = []
        self.solution_path = []
        self.cells = [[]]
        self.texts = [[]]
        self.step = 0

        # 64 length green to yellow to red gradient
        self.heat_gradient = ['#79FE48', '#7EFE47', '#83FE47', '#88FE46', '#8DFE46', '#92FE45', '#96FE45', '#9BFE44',
                              '#A0FE44', '#A5FE43', '#AAFE43', '#AFFE42', '#B4FE42', '#BAFE41', '#BFFE41', '#C4FE40',
                              '#C9FE40', '#CEFE3F', '#D3FE3F', '#D9FE3E', '#DEFE3E', '#E3FE3D', '#E9FE3D', '#EEFE3C',
                              '#F3FE3C', '#F9FE3B', '#FEFD3B', '#FEF83A', '#FEF33A', '#FEED39', '#FEE739', '#FEE238',
                              '#FEDC38', '#FED737', '#FED137', '#FECB36', '#FEC636', '#FEC035', '#FEBA35', '#FEB434',
                              '#FEAE34', '#FEA933', '#FEA333', '#FE9D32', '#FE9732', '#FE9131', '#FE8B31', '#FE8530',
                              '#FE7F30', '#FE792F', '#FE732F', '#FE6C2E', '#FE662E', '#FE602D', '#FE5A2D', '#FE542C',
                              '#FE4D2C', '#FE472B', '#FE412B', '#FE3A2A', '#FE342A', '#FE2D29', '#FE292B', '#FF2830']

        self.create_gui()

        global cancel_animation_id
        cancel_animation_id = None
        global cancel_animation_id_2
        cancel_animation_id_2 = None

    def create_gui(self):
        # Initiating string variables to bind to various GUI components
        self.selected_mode = StringVar(self)
        self.selected_map = StringVar(self)
        self.map_data = StringVar(self)

        # Setting default values
        self.selected_mode.set("A*")
        self.selected_map.set("map1.txt")

        # Creating the GUI components
        group_options = LabelFrame(self, text="Options", padx=5, pady=5)
        group_custom_map = LabelFrame(self, text="Custom Map Input", padx=5, pady=5)
        group_stats = LabelFrame(self, text="Stats", padx=5, pady=190)

        mode_menu = OptionMenu(group_options, self.selected_mode, "A*", "Breadth-first", "Depth-first",
                               command=self.reset_grid(matrix=None))

        map_menu = OptionMenu(group_options, self.selected_map, "map1.txt", "map2.txt", "map3.txt", "map4.txt",
                              "map5.txt", command=lambda matrix: self.reset_grid(open("modul1/"+matrix).readlines()))

        # Buttons
        start_btn = Button(group_options, text="Solve", fg="green", command=self.start_program)
        exit_btn = Button(group_options, text="Exit", fg="red", command=self.quit)
        load_custom_map_btn = Button(group_custom_map, text="Load custom map", command=self.load_custom_map)

        self.custom_map_field = Text(group_custom_map, width=20, height=10, highlightbackground='black',
                                     highlightthickness=1)

        # Stats and numbers
        self.label_time = Label(group_stats, text="Time:")
        self.label_steps = Label(group_stats, text="Steps:")
        self.label_open = Label(group_stats, text="Opened nodes:")
        self.label_closed = Label(group_stats, text="Closed nodes:")
        self.display_time = Label(group_stats, text="0.00")
        self.display_steps = Label(group_stats, text="0")
        self.display_open = Label(group_stats, text="0")
        self.display_closed = Label(group_stats, text="0")

        # Placing components in a grid
        group_options.grid(row=0, column=0, sticky=W+E)
        map_menu.grid(row=0, column=1, padx=0)
        mode_menu.grid(row=0, column=0, padx=0, sticky=W)
        start_btn.grid(row=0, column=2)
        exit_btn.grid(row=0, column=5, sticky=E)

        self.group_view.grid(row=1, column=0)
        self.canvas.grid(row=0, column=0)

        group_custom_map.grid(row=0, column=1, rowspan=2, sticky=N)
        self.custom_map_field.grid(row=0, column=0, sticky=N)
        load_custom_map_btn.grid(row=1, column=0, sticky=E+W)

        group_stats.grid(row=1, column=1, sticky=E+S+W)
        self.label_time.grid(row=0, column=0, sticky=W)
        self.label_steps.grid(row=1, column=0, sticky=W)
        self.label_open.grid(row=2, column=0, sticky=W)
        self.label_closed.grid(row=3, column=0, sticky=W)
        self.display_time.grid(row=0, column=1, sticky=E)
        self.display_steps.grid(row=1, column=1, sticky=E)
        self.display_open.grid(row=2, column=1, sticky=E)
        self.display_closed.grid(row=3, column=1, sticky=E)

        # Configuring components
        mode_menu.configure(width=15)
        map_menu.configure(width=15)
        start_btn.configure(width=8)

        # Calls the method which creates the GUI grid based on the default map
        self.create_grid(self.selected_map.get(), is_file=True)

    def create_grid(self, matrix, is_file=False):
        for cell_row in self.cells:
            for cell in cell_row:
                self.canvas.delete(cell)

        for text_row in self.texts:
            for text in text_row:
                self.canvas.delete(text)

        if is_file:
            matrix = list(open('modul1/'+matrix).readlines())

        width = len(matrix)
        height = len(matrix[0])
        self.cells = [[None for _ in range(height)] for _ in range(width)]
        self.texts = [[None for _ in range(height)] for _ in range(width)]

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
                        matrix[block[1]][block[0]] = '#'

            matrix[start_node[1]][start_node[0]] = 'A'
            matrix[goal_node[1]][goal_node[0]] = 'B'

            self.board = matrix.reverse()
            self.reset_grid(matrix)

        except Exception as e:
            print("Invalid map data:", e)

    def create_solution_grid(self, solution):
        if type(solution) == str:
            self.create_grid(solution)
            return

        matrix = solution['state']
        min_f = self.problem.h(min([min(node_list, key=lambda n: self.problem.h(n)) for node_list in matrix],
                                   key=lambda n: self.problem.h(n))) or 1
        max_f = self.problem.h(max([max(node_list, key=lambda n: self.problem.h(n)) for node_list in matrix],
                                   key=lambda n: self.problem.h(n))) or 1
        max_f -= min_f

        open_nodes = solution['open']

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
                                                                     fill=self.get_heat_color(node, max_f), tags='oval')

                if len(self.texts) > node.x:
                    if len(self.texts[node.x]) > node.y:
                        self.canvas.delete(self.texts[node.x][node.y])
                self.texts[node.x][node.y] = self.canvas.create_text(node.x*30+15, node.y*30+15, text="%d2" % node.f())
        elif node.closed:
            if self.canvas.gettags(self.cells[node.x][node.y]) != 'rectangle':
                self.canvas.delete(self.cells[node.x][node.y])
                self.cells[node.x][node.y] = self.canvas.create_rectangle(
                    node.x*30, node.y*30, (node.x+1)*30, (node.y+1)*30,
                    fill=self.get_heat_color(node, max_f), tags='rectangle')

                if len(self.texts) > node.x:
                    if len(self.texts[node.x]) > node.y:
                        self.canvas.delete(self.texts[node.x][node.y])
                self.texts[node.x][node.y] = self.canvas.create_text(node.x*30+15, node.y*30+15, text="%d2" % node.f())

    def get_heat_color(self, node, max_f):
        weight = float(self.problem.h(node))
        heat_length = float(len(self.heat_gradient))
        if weight == 0 or weight is None:
            pos = 0
        else:
            pos = math.floor(heat_length - ((heat_length / max_f) * weight))
        color = self.heat_gradient[pos]
        return color

    def draw_solution_path(self, node):
        self.canvas.itemconfig(self.cells[node.x][node.y], fill='blue')

    def begin_solution_animation(self):
        global cancel_animation_id
        self.reset_grid(self.board)
        ms_delay = math.floor(500 / float(len(self.solutions)))
        cancel_animation_id = self.after(
            ms_delay, self.update_solution_animation, None, self.solutions, ms_delay, 0)

    def update_solution_animation(self, label, ani_step, ms_delay, frame_num):

        self.display_steps.configure(text=self.step)
        #self.display_open.configure(text='%s' % state['open'])
        #self.display_closed.configure(text='%s' % state['closed'])

        global cancel_animation_id
        if frame_num == len(ani_step):
            if self.problem.solution.found:
                self.animate_solution_path()
            else:
                self.cancel_animation()
            return

        self.create_solution_grid(ani_step[frame_num])
        frame_num = (frame_num + 1) % (len(ani_step) + 1)
        cancel_animation_id = self.after(
            ms_delay, self.update_solution_animation, label, ani_step, ms_delay, frame_num)

    def animate_solution_path(self):
        global cancel_animation_id
        ms_delay = math.floor(250 / float(len(self.solution_path)))
        cancel_animation_id = self.after(
            ms_delay, self.update_solution_path_animation, None, self.solution_path, ms_delay, 0)

    def update_solution_path_animation(self, label, ani_step, ms_delay, frame_num):
        global cancel_animation_id
        if frame_num == len(ani_step):
            self.cancel_animation()
            return

        self.draw_solution_path(ani_step[frame_num])
        frame_num = (frame_num + 1) % (len(ani_step) + 1)
        cancel_animation_id = self.after(
            ms_delay, self.update_solution_path_animation, label, ani_step, ms_delay, frame_num)

    def reset_grid(self, matrix=None):
        if matrix:
            self.cancel_animation()
            self.create_grid(matrix)
            self.board = matrix
        else:
            self.create_grid(self.selected_map.get(), is_file=True)

    def cancel_animation(self):
        global cancel_animation_id
        if cancel_animation_id is not None:
            self.after_cancel(cancel_animation_id)
            cancel_animation_id = None
            return

    # Method for starting the application with the chosen algorithm
    def start_program(self):
        if not self.board:
            self.board = list(open('modul1/'+self.selected_map.get()).readlines())
        self.problem = Board(list(self.board))

        if self.selected_mode.get() == 'A*':
            self.problem.solve(a_star)
        elif self.selected_mode.get() == 'Breadth-first':
            self.problem.solve(breadth_first_search)
        elif self.selected_mode.get() == 'Depth-first':
            self.problem.solve(depth_first_search)

        self.problem.pretty_print()

        self.solutions = self.problem.solution.states
        self.step = self.problem.solution.steps
        self.solution_path = list(reversed(self.problem.solution['path']))[:-1]
        self.begin_solution_animation()


def main():
    root = Tk()
    app = Astar_program(master=root)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    app.mainloop()

main()









