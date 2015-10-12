from tkinter import *
from tkinter import filedialog


class Gui(Frame):
    def __init__(self, nono, gs,  matrix,  master=None):
        Frame.__init__(self, master)
        self.nono = nono
        self.gs = gs
        self.matrix = matrix
        self.master.title("Nonogram Solver")
        self.pack()
        self.canvas = None
        self.selected_scenario = None
        self.btn_load = None
        self.cells = [[]]
        self.create_gui()

    def create_gui(self):
        # Initializing the variables the option menus will use
        self.selected_scenario = StringVar(self)

        # Setting default values for option menu variables
        self.selected_scenario.set("scenario0.txt")

        # Creating the GUI components
        group_state = LabelFrame(self, text="State", padx=5, pady=5)
        group_stats = LabelFrame(self, text="Stats", padx=40, pady=5)
        group_options = LabelFrame(self, text="Options", padx=5, pady=5)
        self.canvas = Canvas(group_state, width=600, height=600, bg="#F0F0F0", highlightbackground="black",
                             highlightthickness=1)
        scenario_menu = OptionMenu(group_options, self.selected_scenario, "scenario0.txt", "scenario1.txt", "scenario2.txt",
                                "scenario3.txt", "scenario4.txt", "scenario5.txt", "scenario6.txt",)

        btn_start = Button(group_options, text="Start", padx=5, pady=5, bg="light green")
        btn_exit = Button(group_options, text="Exit", padx=5, pady=5, bg="red", command=self.quit)
        self.btn_load = Button(group_options, text="Load graph", padx=5, pady=5, command=self.load_scenario)

        # Placing GUI components in a grid
        group_options.grid(row=0, column=0, columnspan=2, sticky=W+E)
        group_state.grid(row=1, column=0)
        group_stats.grid(row=1, column=1, sticky=N+S)

        group_options.grid_columnconfigure(1, weight=1)

        scenario_menu.grid(row=0, column=0, sticky=N+E+S+W)
        self.canvas.grid(row=0, column=0)
        btn_start.grid(row=0, column=5, sticky=E)
        btn_exit.grid(row=0, column=6, sticky=E)

        self.paint_scenario(self.matrix)

    def paint_scenario(self, matrix):
        y = -1
        for line in matrix:
            x = -1
            y += 1
            for item in line:
                x += 1
                if not item:
                    self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill="white",
                                                                    tags='rectangle')
                elif item:
                    self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill="blue",
                                                                    tags='rectangle')
    '''
    def load_scenario(self):
        file = filedialog.askopenfilename(parent=self, filetypes=[('Text Files', '.txt')],
                                          title='Select a scenario file')

        file = file.split('/')[-1]
        self.paint_scenario(file)
    '''




