from tkinter import *
from modul2.vcgraph_problem import VertexColoringProblem
from modul2.search import GraphSearch, Agenda
from copy import deepcopy


class Gui(Frame):
    def __init__(self, vcp,  master=None):
        Frame.__init__(self, master)
        self.csp = vcp
        self.vcp = VertexColoringProblem()
        self.vcp.set_graph()
        self.gs = GraphSearch(vcp, frontier=Agenda)

        self.master.title("VC problem")
        self.pack()
        self.canvas = None
        self.colors = {0: "#FF0000", 1: "#33CC33", 2: "#3366CC", 3: "#FFFF00", 4: "#FF6600", 5: "#FF3399",
                       6: "#993300", 7: "#990033", 8: "#808080", 9: "#99FFCC", 10: "#000000"}

        self.graph_nodes = []
        self.create_gui()
        self.csp = None


    def create_gui(self):
        # Initializing the variables the option menus will use
        self.selected_graph = StringVar(self)
        self.selected_k_value = StringVar(self)

        # Setting default values for option menu variables
        self.selected_graph.set("modul2/graph1.txt")
        self.selected_k_value.set(3)

        # Creating the GUI components
        group_state = LabelFrame(self, text="State", padx=5, pady=5)
        group_stats = LabelFrame(self, text="Stats", padx=40, pady=5)
        group_options = LabelFrame(self, text="Options", padx=5, pady=5)
        self.canvas = Canvas(group_state, width=600, height=600, bg="#F0F0F0", highlightbackground="black",
                             highlightthickness=1)
        graph_menu = OptionMenu(group_options, self.selected_graph, "modul2/graph1.txt", "modul2/graph2.txt",
                                "modul2/graph3.txt", "modul2/graph4.txt", "modul2/graph5.txt", "modul2/graph6.txt",)

        k_value_menu = OptionMenu(group_options, self.selected_k_value, 4, 5, 6)
        label_colored_nodes = Label(group_stats, text="0/0")
        btn_start = Button(group_options, text="Start", padx=5, pady=5, bg="light green", command=self.search)
        btn_exit = Button(group_options, text="Exit", padx=5, pady=5, bg="red", command=self.quit)

        # Placing GUI components in a grid
        group_options.grid(row=0, column=0, columnspan=2, sticky=W+E)
        group_state.grid(row=1, column=0)
        group_stats.grid(row=1, column=1, sticky=N+S)

        group_options.grid_columnconfigure(1, weight=1)

        graph_menu.grid(row=0, column=0, sticky=N+E+S+W)
        k_value_menu.grid(row=0, column=1, sticky=W)
        self.canvas.grid(row=0, column=0)
        label_colored_nodes.grid(row=0, column=0)
        btn_start.grid(row=0, column=5, sticky=E)
        btn_exit.grid(row=0, column=6, sticky=E)

        self.graph_nodes = list(self.csp.node_domain_map.keys())
        print(self.graph_nodes)
        self.paint_graph(self.csp)

    def search(self):
        self.vcp.set_graph(open(self.selected_graph.get()), int(self.selected_k_value.get()))
        self.paint_graph(self.vcp)

        vc_nodes, found = self.gs.search()

        if found:
            self.paint_solution(vc_nodes)
        else:
            self.paint_error()
            print("Fant ikke løsning, kis (jeg er i gui.py)")

    def update_graph_node(self, vcp, node):
        self.canvas.itemconfig(self.graph_nodes[node], fill=self.colors[vcp.node_domain_map[node][0]])

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
            print('cooooordinates', node_id)
            self.update_graph_node(vc_node, node_id)

            #self.canvas.create_oval(coordinates[node][0], coordinates[node][1],
            #                        coordinates[node][0] + 15, coordinates[node][1] + 15,
            #                        fill=self.colors[final_node.node_domain_map[node][0]])

    def paint_error(self):
        pass

    def paint_graph(self, vcp):
        self.csp.coordinates = self.scale_coords(self.get_graph_dims(self.csp), self.csp)

        for i in range(0, len(vcp.constraints)):
            start_x = vcp.coordinates[int(vcp.constraints[i].variables[0])][0]
            start_y = vcp.coordinates[int(vcp.constraints[i].variables[0])][1]
            end_x = vcp.coordinates[int(vcp.constraints[i].variables[1])][0]
            end_y = vcp.coordinates[int(vcp.constraints[i].variables[1])][1]

            self.canvas.create_line(start_x+7.5, start_y+7.5, end_x+7.5, end_y+7.5)

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
            x_scale = (int(self.canvas['width'])-20) / (10 + (x_offset + dim['max_x']) * 15)
        if (10 + (y_offset + dim['max_y']) * 15) > (int(self.canvas['height']) - 10):
            y_scale = (int(self.canvas['height'])-20) / (10 + (y_offset + dim['max_y']) * 15)

        scaled_coordinates = {}
        for i in vcp.coordinates:
            scaled_coordinates[i] = [(10 + (x_offset + vcp.coordinates[i][0]) * 15) * x_scale,
                                     (10 + (y_offset + vcp.coordinates[i][1]) * 15) * y_scale]

        return scaled_coordinates






