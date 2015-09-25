from tkinter import *


class Gui(Frame):
    def __init__(self, csp,  master=None):
        Frame.__init__(self, master)
        self.csp = csp
        self.master.title("VC problem")
        self.pack()
        self.canvas = Canvas(self, width=1366, height=768, highlightbackground='black', highlightthickness=1)
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
        print(len(self.csp.nodes))
        for node in self.csp.nodes:
            node.xPos = float(node.xPos) * 20
            node.yPos = float(node.yPos) * 20
            self.canvas.create_oval(node.xPos, node.yPos, node.xPos+10, node.yPos+10, fill="red")

        for i in range(0, len(self.csp.constraints)):
            start_x = self.csp.nodes[int(self.csp.constraints[i][0])].xPos
            start_y = self.csp.nodes[int(self.csp.constraints[i][0])].yPos
            end_x = self.csp.nodes[int(self.csp.constraints[i][1])].xPos
            end_y = self.csp.nodes[int(self.csp.constraints[i][1])].yPos

            self.canvas.create_line(start_x+5, start_y+5, end_x+5, end_y+5)









