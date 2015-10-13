from tkinter import *
from tkinter import filedialog
from modul2.vcgraph_problem import VertexColoringProblem
from algorithms.search import GraphSearch, Agenda
from copy import deepcopy
import time

import threading
from queue import Queue


class ThreadedDrawer(threading.Thread):
    def __init__(self, frame, queue, stopper):
        threading.Thread.__init__(self)
        self.frame = frame
        self.queue = queue
        self.stopper = stopper

    def run(self):
        prev_set = set()
        i = 0
        while True:
            if self.stopper.is_set():
                self.frame.recreate()
                self.frame.btn_start.config(state='normal')
                break
            temp_set = set()
            state = self.queue.get()
            i += 1

            if state['solved']:

                top = Toplevel()
                top.geometry("%dx%d%+d%+d" % (250, 100, 250, 200))
                top.title("Success!")
                msg = Message(top, text="Graph successfully solved!")
                msg.pack()
                btn_ok = Button(top, text="Ok", command=top.destroy)
                btn_ok.pack()

                self.frame.btn_start.config(state='normal')

                self.stopper.set()
                break

            # Calculating stats and numbers for the solved / not solved graph
            unsatisfied = []
            u_counter = 0
            m_counter = 0
            for t in state['node'].node_domain:
                unsatisfied.append(state['node'].node_domain[t])
            for value in unsatisfied:
                if not value:
                    u_counter += 1
                elif len(value) > 1:
                    m_counter += 1

            total_nodes = state['open'] + state['closed']
            closed = state['closed'] - 1

            self.frame.steps.configure(text='%i' % total_nodes)
            self.frame.open_c.configure(text='%s' % state['open'])
            self.frame.closed_c.configure(text='%s' % closed)
            self.frame.path_length.configure(text='%s' % state['closed'])
            self.frame.missing_colors.configure(text='%s' % m_counter)
            self.frame.unsatisfied_cons.configure(text='%s' % u_counter)

            for node, domain in state["node"].node_domain.items():
                temp_set.add((node, frozenset(domain)))
            temp_set = frozenset(temp_set)

            node_domain = temp_set.difference(prev_set)
            prev_set = temp_set

            for gac_node, domain in node_domain:
                self.frame.update_graph_node(gac_node, list(domain)[0])


class ThreadedSearch(threading.Thread):
    def __init__(self, frame, queue, search, stopper, timeywimey):
        threading.Thread.__init__(self)
        self.frame = frame
        self.queue = queue
        self.search = search
        self.stopper = stopper
        self.timeywimey = timeywimey

    def run(self):
        while True:
            if self.stopper.is_set():
                self.queue.put('stop')
                self.frame.timer.configure(text='%.2f s' % (time.time() - self.timeywimey))
                break
            try:
                state = next(self.search)
                self.queue.put(state)
            except StopIteration:
                self.queue.put('stop')
                self.frame.timer.configure(text='%.2f s' % (time.time() - self.timeywimey))
                break


class Gui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("Vertex Color Problem")
        self.pack()
        self.vcp = VertexColoringProblem()
        self.vcp.set_graph()
        self.gs = GraphSearch(self.vcp, frontier=Agenda)
        self.solution_queue = Queue()
        self.graph_nodes = {}
        self.edges = []

        self.colors = {0: "#FF0000", 1: "#33CC33", 2: "#3366CC", 3: "#FFFF00", 4: "#FF6600", 5: "#FF3399",
                       6: "#993300", 7: "#990033", 8: "#808080", 9: "#99FFCC", 10: "#9900DD", 11: "#000000"}

        self.canvas = None
        self.btn_start = None
        self.timer = None
        self.steps = None
        self.open_c = None
        self.closed_c = None
        self.path_length = None
        self.missing_colors = None
        self.label_timer = None
        self.label_steps = None
        self.label_open = None
        self.label_closed = None
        self.label_path_length = None
        self.label_unsatisfied_cons = None
        self.unsatisfied_cons = None
        self.btn_load = None
        self.input_function = None
        self.input_function_field = None
        self.label_missing_colors = None

        self.td = None
        self.ts = None

        self.selected_graph = None
        self.selected_k_value = None

        self.thread_stopper = threading.Event()
        self.thread_stopper.set()

        self.create_gui()

    def create_gui(self):
        # Initializing the variables the option menus will use
        self.selected_graph = StringVar(self)
        self.selected_k_value = StringVar(self)
        self.input_function = StringVar(self)

        # Setting default values for option menu variables
        self.selected_graph.set("graph1.txt")
        self.input_function.set("x!=y")
        self.selected_k_value.set(4)

        # Creating the GUI components
        group_state = LabelFrame(self, text="State", padx=5, pady=5)
        group_stats = LabelFrame(self, text="Stats", padx=40, pady=5)
        group_options = LabelFrame(self, text="Options", padx=5, pady=5)

        self.canvas = Canvas(group_state, width=600, height=600, bg="#F0F0F0", highlightbackground="black",
                             highlightthickness=1)
        graph_menu = OptionMenu(group_options, self.selected_graph, "graph1.txt", "graph2.txt",
                                "graph3.txt", "graph4.txt", "graph5.txt", "graph6.txt", command=self.change)
        k_value_menu = OptionMenu(group_options, self.selected_k_value, 3, 4, 5, 6, 7, 8, 9, 10, command=self.change)

        self.input_function_field = Entry(group_options)
        self.input_function_field.insert(0, 'x!=y')
        label_input_function = Label(group_options, text="Input function:")

        self.timer = Label(group_stats, text="0.00")

        self.btn_start = Button(group_options, text="Start", padx=5, pady=5, bg="light green", command=self.thready_search)

        btn_exit = Button(group_options, text="Exit", padx=5, pady=5, bg="red", command=self.exit)
        self.btn_load = Button(group_options, text="Load graph", padx=5, pady=5, command=self.load_graph)


        # Stats
        self.label_timer = Label(group_stats, text="Time:")
        self.label_steps = Label(group_stats, text="Total GAC-nodes in tree:")
        self.label_open = Label(group_stats, text="Opened GAC nodes:")
        self.label_closed = Label(group_stats, text="Popped and expanded nodes:")
        self.label_path_length = Label(group_stats, text="Path length:")
        self.label_missing_colors = Label(group_stats, text="Vertices missing color:")
        self.label_unsatisfied_cons = Label(group_stats, text="Unsatisfied constraints:")
        self.steps = Label(group_stats, text="0")
        self.open_c = Label(group_stats, text="0")
        self.closed_c = Label(group_stats, text="0")
        self.path_length = Label(group_stats, text="0")
        self.missing_colors = Label(group_stats, text="0")
        self.unsatisfied_cons = Label(group_stats, text="0")

        # Placing GUI components in a grid
        group_options.grid(row=0, column=0, columnspan=2, sticky=W + E)
        group_state.grid(row=1, column=0)
        group_stats.grid(row=1, column=1, sticky=N + S)

        group_options.grid_columnconfigure(1, weight=1)

        graph_menu.grid(row=0, column=0, sticky=N + E + S + W)
        k_value_menu.grid(row=0, column=1, sticky=W)
        label_input_function.grid(row=0, column=2)
        self.input_function_field.grid(row=0, column=3)
        self.btn_load.grid(row=0, column=4, sticky=W)

        self.canvas.grid(row=0, column=0)
        self.label_timer.grid(row=1, column=0, sticky=W)
        self.label_steps.grid(row=2, column=0, sticky=W)
        self.label_closed.grid(row=3, column=0, sticky=W)
        self.label_path_length.grid(row=4, column=0, sticky=W)
        self.label_missing_colors.grid(row=5, column=0, sticky=W)
        self.label_unsatisfied_cons.grid(row=6, column=0, sticky=W)

        self.timer.grid(row=1, column=1, sticky=E)
        self.steps.grid(row=2, column=1, sticky=E)
        self.missing_colors.grid(row=5, column=1, sticky=E)
        self.unsatisfied_cons.grid(row=6, column=1, sticky=E)
        self.closed_c.grid(row=3, column=1, sticky=E)
        self.path_length.grid(row=4, column=1, sticky=E)
        self.btn_start.grid(row=0, column=5, sticky=E)
        btn_exit.grid(row=0, column=6, sticky=E)

        self.change()

    def change(self, _=None):
        if self.thread_stopper.is_set():
            self.recreate()
        else:
            self.thread_stopper.set()
            self.recreate()

    def recreate(self, graph=None):
        self.clear_grid()
        self.vcp = VertexColoringProblem()
        if not graph:
            graph = self.selected_graph.get()
        self.vcp.set_graph(graph, self.selected_k_value.get())

        self.create_grid()
        self.create_graph()
        self.gs = GraphSearch(problem=self.vcp, frontier=Agenda)

    def clear_grid(self):
        self.canvas.delete("all")

    def create_grid(self):
        self.clear_grid()
        self.graph_nodes = deepcopy(self.vcp.node_domain)

    def create_graph(self):
        vcp = self.vcp
        self.vcp.coordinates = self.scale_coords(self.get_graph_dims(vcp), vcp)

        for i in range(0, len(vcp.constraints)):
            start_x = vcp.coordinates[int(vcp.constraints[i].variables[0])][0]
            start_y = vcp.coordinates[int(vcp.constraints[i].variables[0])][1]
            end_x = vcp.coordinates[int(vcp.constraints[i].variables[1])][0]
            end_y = vcp.coordinates[int(vcp.constraints[i].variables[1])][1]

            self.edges.append(self.canvas.create_line(start_x + 3.75, start_y + 3.75, end_x + 3.75, end_y + 3.75))

        for i in vcp.coordinates:
            c = 11 if len(vcp.get_domain(i)) > 1 else vcp.get_domain(i)[0]
            self.graph_nodes[i] = self.canvas.create_oval(vcp.coordinates[i][0], vcp.coordinates[i][1],
                                                          vcp.coordinates[i][0] + 7.5, vcp.coordinates[i][1] + 7.5,
                                                          fill=self.colors[c],
                                                          tags=c)

    def thready_search(self):
        #self.change()
        self.timer.config(text="0.00")
        self.thread_stopper.clear()
        self.solution_queue = Queue()
        self.td = ThreadedDrawer(self, self.solution_queue, self.thread_stopper)
        self.td.start()
        self.ts = ThreadedSearch(self, self.solution_queue, self.gs.search_yieldie(), self.thread_stopper, time.time())
        self.ts.start()
        self.btn_start.config(state='disabled')

    def update_graph_node(self, node, domain):
        self.canvas.itemconfig(self.graph_nodes[node], fill=self.colors[domain])

    def paint_graph(self, vcp):
        vcp.coordinates = self.scale_coords(self.get_graph_dims(vcp), vcp)

        for i in vcp.coordinates:
            self.graph_nodes[i] = self.canvas.create_oval(vcp.coordinates[i][0], vcp.coordinates[i][1],
                                                          vcp.coordinates[i][0] + 15, vcp.coordinates[i][1] + 15,
                                                          fill=self.colors[vcp.get_domain(i)[0]])
        for i in range(0, len(vcp.constraints)):
            start_x = vcp.coordinates[int(vcp.constraints[i].variables[0])][0]
            start_y = vcp.coordinates[int(vcp.constraints[i].variables[0])][1]
            end_x = vcp.coordinates[int(vcp.constraints[i].variables[1])][0]
            end_y = vcp.coordinates[int(vcp.constraints[i].variables[1])][1]

            self.canvas.create_line(start_x + 7.5, start_y + 7.5, end_x + 7.5, end_y + 7.5)

    def get_graph_dims(self, vcp):
        """
        Method to get the maximum and minimum coordinates of the vertices in the graph
        for scaling the graph to the Tkinter canvas
        :param vcp: Takes in a complete vcp problem
        :return: A dictionary with required values to scale the graph
        """
        x_positions, y_positions = [], []
        for i in vcp.coordinates:
            x_positions.append(vcp.coordinates[i][0])
            y_positions.append(vcp.coordinates[i][1])

        max_x = max(x_positions)
        max_y = max(y_positions)
        min_x = min(x_positions)
        min_y = min(y_positions)
        canvas_width = self.canvas['width']
        canvas_height = self.canvas['height']
        dimensions = {"max_x": max_x, "max_y": max_y, "min_x": min_x, "min_y": min_y,
                      "c_width": canvas_width, "c_height": canvas_height}
        return dimensions

    def scale_coords(self, dim, vcp):
        """
        Method to do the actual scaling
        :param dim: Dictionary with max and min coordinates for vertices, and canvas size
        :param vcp: Complete vcp problem
        :return:
        """
        dim = dim
        x_scale, y_scale = 1, 1
        x_offset, y_offset = 0, 0
        if dim['min_x'] < 0:
            x_offset = -dim['min_x']
        if dim['min_y'] < 0:
            y_offset = -dim['min_y']

        if (10 + (x_offset + dim['max_x']) * 15) > (int(self.canvas['width']) - 10):
            x_scale = (int(self.canvas['width']) - 20) / (10 + (x_offset + dim['max_x']) * 15)
        if (10 + (y_offset + dim['max_y']) * 15) > (int(self.canvas['height']) - 10):
            y_scale = (int(self.canvas['height']) - 20) / (10 + (y_offset + dim['max_y']) * 15)

        scaled_coordinates = {}
        for i in vcp.coordinates:
            scaled_coordinates[i] = [(10 + (x_offset + vcp.coordinates[i][0]) * 15) * x_scale,
                                     (10 + (y_offset + vcp.coordinates[i][1]) * 15) * y_scale]

        return scaled_coordinates

    def load_graph(self):
        file = filedialog.askopenfilename(parent=self, filetypes=[('Text Files', '.txt')],
                                          title='Select a graph file')

        file = file.split('/')[-1]
        self.recreate(file)

    def exit(self):
        self.change()
        self.after(500, self.quit)







