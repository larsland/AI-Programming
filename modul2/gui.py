from tkinter import *


class Gui(Frame):
    def __init__(self, csp,  master=None):
        Frame.__init__(self, master)
        self.csp = csp
        self.master.title("VC problem")
        self.pack()
        self.canvas = Canvas(self, width=800, height=600, highlightbackground='black', highlightthickness=1)
        #self.canvas.configure(scrollregion=(self.canvas.bbox("all")))
        self.selected_graph = None
        self.selected_k_value = None
        self.create_gui()
        self.csp = None

    def create_gui(self):
        self.selected_graph = StringVar(self)
        self.selected_k_value = StringVar(self)

        self.selected_graph.set("graph1.txt")
        self.selected_k_value.set(4)

        graph_menu = OptionMenu(self, self.selected_graph, "graph1.txt", "graph2.txt", "graph3.txt", "graph4.txt",
                                "graph5.txt", "graph6.txt")
        k_value_menu = OptionMenu(self, self.selected_k_value, 4, 5, 6)

        graph_menu.grid(row=0, column=0, sticky=W)
        k_value_menu.grid(row=0, column=1)
        self.canvas.grid(row=1, column=0, columnspan=2)

        self.paint_graph()

    def paint_graph(self):
        dim = self.get_graph_dims()
        self.get_graph_dims()
        for node in self.csp.nodes:
            node.xPos = float(node.xPos) * 20
            node.yPos = float(node.yPos) * 20
            self.canvas.create_oval(node.xPos, node.yPos, node.xPos+15, node.yPos+15, fill=node.color)
            self.canvas.create_text(node.xPos+7, node.yPos+7, text=str(node.id))

        for i in range(0, len(self.csp.constraints)):
            start_x = self.csp.nodes[int(self.csp.constraints[i].variables[0])].xPos
            start_y = self.csp.nodes[int(self.csp.constraints[i].variables[0])].yPos
            end_x = self.csp.nodes[int(self.csp.constraints[i].variables[1])].xPos
            end_y = self.csp.nodes[int(self.csp.constraints[i].variables[1])].yPos

            self.canvas.create_line(start_x+10, start_y+10, end_x+10, end_y+10)

    def get_graph_dims(self):
        x_positions, y_positions = [], []
        for node in self.csp.nodes:
            x_positions.append(node.xPos)
            y_positions.append(node.yPos)
        max_x = max(x_positions)
        max_y = max(y_positions)
        min_x = min(x_positions)
        min_y = min(y_positions)
        canvas_width = self.canvas['width']
        canvas_height = self.canvas['height']

        dimensions = {"max_x": max_x, "max_y": max_y, "min_x": min_x, "min_y": min_y,
                      "c_width": canvas_width, "c_height": canvas_height}

        return dimensions
















