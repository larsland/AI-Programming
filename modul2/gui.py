from tkinter import *
from modul2.vcgraph_problem import VertexColoringProblem
from modul2.search import GraphSearch, Agenda
from copy import deepcopy
import time

import threading
from queue import Queue, Empty

global cancel_clock_id


class ThreadedDrawer(threading.Thread):
    def __init__(self, frame, queue, stopper):
        threading.Thread.__init__(self)
        self.queue = queue
        self.frame = frame
        self.stopper = stopper

    def run(self):
        prev_set = set()
        while True:
            t = time.time()
            if self.stopper.is_set():
                self.frame.recreate()
                self.frame.btn_start.config(state='normal')
                break
            temp_set = set()
            vc_node = self.queue.get()
            if vc_node == 'stop':
                print('done.')

                top = Toplevel()
                top.geometry("%dx%d%+d%+d" % (300, 200, 250, 200))
                top.title("Success!")
                msg = Message(top, text="Graph successfully solved in: ")
                msg.pack()
                msg_time = Message(top, text=t)
                msg_time.pack()
                btn_ok = Button(top, text="Ok", command=top.destroy)
                btn_ok.pack()

                self.frame.btn_start.config(state='normal')
                break

            for node, domain in vc_node.node_domain_map.items():
                temp_set.add((node, frozenset(domain)))
            temp_set = frozenset(temp_set)

            #graph_nodes = deepcopy(self.frame.graph_nodes)
            #print(int(self.frame.canvas.gettags(graph_nodes[0])[0]))
            #break

            node_domain = temp_set.difference(prev_set)
            prev_set = temp_set
            #node_domain = [(gac_node, domain) if len(domain) > 1 else
            #               (gac_node, [11]) for gac_node, domain in node_domain]
            for gac_node, domain in node_domain:
                self.frame.update_graph_node(gac_node, list(domain)[0])


class ThreadedSearch(threading.Thread):
    def __init__(self, queue, search, stopper, frame):
        threading.Thread.__init__(self)
        self.queue = queue
        self.search = search
        self.stopper = stopper
        self.frame = frame

    def run(self):
        while True:
            if self.stopper.is_set():
                self.queue.put('stop')
                self.frame.cancel_clock()
                break
            try:
                node = next(self.search)
                self.queue.put(node)
            except StopIteration:
                self.queue.put('stop')
                self.frame.cancel_clock()
                break


class Gui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.vcp = VertexColoringProblem()
        self.vcp.set_graph()
        self.gs = GraphSearch(self.vcp, frontier=Agenda)

        self.solution_queue = Queue()

        self.master.title("VC problem")
        self.pack()
        self.canvas = None
        self.colors = {0: "#FF0000", 1: "#33CC33", 2: "#3366CC", 3: "#FFFF00", 4: "#FF6600", 5: "#FF3399",
                       6: "#993300", 7: "#990033", 8: "#808080", 9: "#99FFCC", 10: "#9900DD", 11: "#000000"}

        self.btn_start = None
        self.timer = None

        self.graph_nodes = {}
        self.edges = []

        self.thread_stopper = threading.Event()
        self.thread_stopper.set()

        global cancel_clock_id
        cancel_clock_id = None

        self.create_gui()

    def cancel_clock(self):
        global cancel_clock_id
        if cancel_clock_id is not None:
            self.after_cancel(cancel_clock_id)
            cancel_clock_id = None
            return

    def begin_clock(self, original=time.time()):
        global cancel_clock_id
        cancel_clock_id = self.after(1000, self.update_clock, original)

    def update_clock(self, original):
        self.timer.configure(text='%.2f' % (time.time() - original))
        global cancel_clock_id
        cancel_clock_id = self.after(1000, self.update_clock, original)

    def create_gui(self):
        # Initializing the variables the option menus will use
        self.selected_graph = StringVar(self)
        self.selected_k_value = StringVar(self)

        # Setting default values for option menu variables
        self.selected_graph.set("graph1.txt")
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
        label_colored_nodes = Label(group_stats, text="0/0")

        self.timer = Label(group_stats, text="poop")
        self.btn_start = Button(group_options, text="Start", padx=5, pady=5, bg="light green", command=self.thready_search)

        btn_exit = Button(group_options, text="Exit", padx=5, pady=5, bg="red", command=self.quit)

        # Placing GUI components in a grid
        group_options.grid(row=0, column=0, columnspan=2, sticky=W + E)
        group_state.grid(row=1, column=0)
        group_stats.grid(row=1, column=1, sticky=N + S)

        group_options.grid_columnconfigure(1, weight=1)

        graph_menu.grid(row=0, column=0, sticky=N + E + S + W)
        k_value_menu.grid(row=0, column=1, sticky=W)
        self.canvas.grid(row=0, column=0)
        label_colored_nodes.grid(row=0, column=0)
        self.timer.grid(row=1, column=0)
        self.btn_start.grid(row=0, column=5, sticky=E)
        btn_exit.grid(row=0, column=6, sticky=E)

        self.change()

    def change(self, woot=None):
        if self.thread_stopper.is_set():
            self.recreate()
        else:
            self.thread_stopper.set()

    def recreate(self):
        self.clear_grid()
        self.vcp = VertexColoringProblem()
        self.vcp.set_graph(self.selected_graph.get(), self.selected_k_value.get())
        self.create_grid()
        self.create_graph()
        self.gs = GraphSearch(problem=self.vcp, frontier=Agenda)

    def clear_grid(self):
        self.canvas.delete("all")

        """
        for edge in self.edges:
            self.canvas.delete(edge)
        self.edges = []
        for node in self.graph_nodes:
            self.canvas.delete(node)
        self.graph_nodes = []
        """

    def create_grid(self):
        self.clear_grid()

        # if is_file:
        self.vcp = VertexColoringProblem()
        self.vcp.set_graph(self.selected_graph.get(), int(self.selected_k_value.get()))

        self.graph_nodes = deepcopy(self.vcp.node_domain_map)


    def create_graph(self):
        vcp = self.vcp
        self.vcp.coordinates = self.scale_coords(self.get_graph_dims(vcp), vcp)

        for i in range(0, len(vcp.constraints)):
            start_x = vcp.coordinates[int(vcp.constraints[i].variables[0])][0]
            start_y = vcp.coordinates[int(vcp.constraints[i].variables[0])][1]
            end_x = vcp.coordinates[int(vcp.constraints[i].variables[1])][0]
            end_y = vcp.coordinates[int(vcp.constraints[i].variables[1])][1]

            self.edges.append(self.canvas.create_line(start_x + 7.5, start_y + 7.5, end_x + 7.5, end_y + 7.5))

        for i in vcp.coordinates:
            c = 11 if len(vcp.get_domain(i)) > 1 else vcp.get_domain(i)[0]
            self.graph_nodes[i] = self.canvas.create_oval(vcp.coordinates[i][0], vcp.coordinates[i][1],
                                                          vcp.coordinates[i][0] + 15, vcp.coordinates[i][1] + 15,
                                                          fill=self.colors[c],
                                                          tags=c)

    def thready_search(self):
        self.thread_stopper.clear()
        self.solution_queue = Queue()
        ThreadedDrawer(self, self.solution_queue, self.thread_stopper).start()
        ThreadedSearch(self.solution_queue, self.gs.search_yieldie(), self.thread_stopper, self).start()
        self.btn_start.config(state='disabled')
        #self.begin_clock(time.time())


    def search(self):
        vc_nodes, found = self.gs.search()
        t4 = time.time()
        # self.vcp = VertexColoringProblem()
        #self.vcp.set_graph(self.selected_graph.get(), self.selected_k_value.get())
        #print(self.selected_graph.get())
        #print(self.selected_k_value.get())
        #self.gs = GraphSearch(self.vcp, frontier=Agenda)

        #vc_nodes, found = self.gs.search()

        print(vc_nodes, found)

        #print("Times: VC_init: %s, GraphSearch_init: %s, search: %s" % (t2-t1, t3-t2, t4-t3))

        #if found:
        #    self.paint_solution(vc_nodes)
        #else:
        #    self.paint_error()
        #    print("Fant ikke løsning, kis (jeg er i gui.py)")


    def update_graph_node(self, node, domain):
        self.canvas.itemconfig(self.graph_nodes[node], fill=self.colors[domain])

    def update_graph_node_2(self, node_domain_map, node):
        self.canvas.itemconfig(self.graph_nodes[node], fill=self.colors[node_domain_map[node][0]])

    def paint_solution(self, vc_nodes, ani_step=-1):
        vc_node = vc_nodes[ani_step]
        # coordinates = self.scale_coords(self.get_graph_dims(final_node), final_node)
        """
        for constraint in final_node.constraints:
            start_x = coordinates[constraint.variables[0]][0]
            start_y = coordinates[constraint.variables[0]][1]
            end_x = coordinates[constraint.variables[1]][0]
            end_y = coordinates[constraint.variables[1]][1]

            self.canvas.create_line(start_x+7.5, start_y+7.5, end_x+7.5, end_y+7.5)
        """
        for node_id in vc_node.coordinates:
            self.update_graph_node(vc_node, node_id)

    def paint_error(self):
        pass

    def paint_graph(self, vcp):
        vcp.coordinates = self.scale_coords(self.get_graph_dims(vcp), vcp)

        for i in range(0, len(vcp.constraints)):
            start_x = vcp.coordinates[int(vcp.constraints[i].variables[0])][0]
            start_y = vcp.coordinates[int(vcp.constraints[i].variables[0])][1]
            end_x = vcp.coordinates[int(vcp.constraints[i].variables[1])][0]
            end_y = vcp.coordinates[int(vcp.constraints[i].variables[1])][1]

            self.canvas.create_line(start_x + 7.5, start_y + 7.5, end_x + 7.5, end_y + 7.5)

        for i in vcp.coordinates:
            self.graph_nodes[i] = self.canvas.create_oval(vcp.coordinates[i][0], vcp.coordinates[i][1],
                                                          vcp.coordinates[i][0] + 15, vcp.coordinates[i][1] + 15,
                                                          fill=self.colors[vcp.get_domain(i)[0]])

    def get_graph_dims(self, vcp):
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






