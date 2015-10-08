from tkinter import *


class Gui(Frame):
    def __init__(self, csp,  master=None):
        Frame.__init__(self, master)
        self.csp = csp
        self.master.title("VC problem")
        self.pack()
        self.canvas = None
        self.selected_graph = None
        self.selected_k_value = None
        self.colors = {0: "#FF0000", 1: "#33CC33", 2: "#3366CC", 3: "#FFFF00", 4: "#FF6600", 5: "#FF3399",
                       6: "#993300", 7: "#990033", 8: "#808080", 9: "#99FFCC"}
        self.create_gui()
        self.csp = None



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
                                "graph3.txt", "graph4.txt", "graph5.txt", "graph6.txt",)

        k_value_menu = OptionMenu(group_options, self.selected_k_value, 4, 5, 6)
        label_colored_nodes = Label(group_stats, text="0/0")
        btn_start = Button(group_options, text="Start", padx=5, pady=5, bg="light green")
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

        self.paint_graph()

    def paint_graph(self):
        self.scale_cords(self.get_graph_dims())

        for i in range(0, len(self.csp.constraints)):
            start_x = self.csp.coordinates[int(self.csp.constraints[i].variables[0])][0]
            start_y = self.csp.coordinates[int(self.csp.constraints[i].variables[0])][1]
            end_x = self.csp.coordinates[int(self.csp.constraints[i].variables[1])][0]
            end_y = self.csp.coordinates[int(self.csp.constraints[i].variables[1])][1]

            self.canvas.create_line(start_x+7.5, start_y+7.5, end_x+7.5, end_y+7.5)

        for i in self.csp.coordinates:
            self.canvas.create_oval(self.csp.coordinates[i][0], self.csp.coordinates[i][1],
                                    self.csp.coordinates[i][0] + 15, self.csp.coordinates[i][1] + 15,
                                    fill=self.colors[self.csp.nodes[i][1]])

    def get_graph_dims(self):
        x_positions, y_positions = [], []
        for i in self.csp.coordinates:
            x_positions.append(self.csp.coordinates[i][0])
            y_positions.append(self.csp.coordinates[i][1])

        max_x = max(x_positions)
        max_y = max(y_positions)
        min_x = min(x_positions)
        min_y = min(y_positions)
        canvas_width = self.canvas['width']
        canvas_height = self.canvas['height']
        dimensions = {"max_x": max_x, "max_y": max_y, "min_x": min_x, "min_y": min_y,
                      "c_width": canvas_width, "c_height": canvas_height}
        return dimensions

    def scale_cords(self, dim):
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

        for i in self.csp.coordinates:
            self.csp.coordinates[i][0] = (10 + (x_offset + self.csp.coordinates[i][0]) * 15) * x_scale
            self.csp.coordinates[i][1] = (10 + (y_offset + self.csp.coordinates[i][1]) * 15) * y_scale






