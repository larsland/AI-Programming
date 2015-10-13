from tkinter import *
from tkinter import filedialog
import time
from algorithms.search import GraphSearch, Agenda
from modul3.nonograms_problem import NonogramProblem


class Gui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("Nonogram Solver")
        self.pack()
        self.nono = NonogramProblem()
        #self.nono.set_scenario('modul3/scenarioes/scenario1.txt')
        self.gs = None

        self.canvas = None
        self.selected_scenario = None
        self.btn_load = None
        self.display_time = None
        self.display_steps = None
        self.display_open = None
        self.display_closed = None
        self.label_time = None
        self.label_steps = None
        self.label_open = None
        self.label_closed = None

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
        scenario_menu = OptionMenu(group_options, self.selected_scenario, "scenario0.txt", "scenario1.txt",
                                   "scenario2.txt", "scenario3.txt", "scenario4.txt", "scenario5.txt", "scenario6.txt",
                                   "sweet-one.txt",
                                   command=self.set_map)

        btn_start = Button(group_options, text="Solve", padx=5, pady=5, bg="light green", command=self.paint_scenario)
        btn_exit = Button(group_options, text="Exit", padx=5, pady=5, bg="red", command=self.quit)
        #self.btn_load = Button(group_options, text="Load graph", padx=5, pady=5, command=self.load_scenario)

        # Stats and numbers
        self.label_time = Label(group_stats, text="Time:")
        self.label_steps = Label(group_stats, text="Steps:")
        self.label_open = Label(group_stats, text="Opened nodes:")
        self.label_closed = Label(group_stats, text="Closed nodes:")
        self.display_time = Label(group_stats, text="0.00")
        self.display_steps = Label(group_stats, text="0")
        self.display_open = Label(group_stats, text="0")
        self.display_closed = Label(group_stats, text="0")

        # Placing GUI components in a grid
        group_options.grid(row=0, column=0, columnspan=2, sticky=W+E)
        group_options.grid_columnconfigure(1, weight=1)
        scenario_menu.grid(row=0, column=0, sticky=N+E+S+W)
        btn_start.grid(row=0, column=5, sticky=E)
        btn_exit.grid(row=0, column=6, sticky=E)

        group_state.grid(row=1, column=0)
        self.canvas.grid(row=0, column=0)

        group_stats.grid(row=1, column=1, sticky=N+S)
        self.label_time.grid(row=0, column=0, sticky=W)
        self.label_steps.grid(row=1, column=0, sticky=W)
        self.label_open.grid(row=2, column=0, sticky=W)
        self.label_closed.grid(row=3, column=0, sticky=W)

        self.display_time.grid(row=0, column=1, sticky=E)
        self.display_steps.grid(row=1, column=1, sticky=E)
        self.display_open.grid(row=2, column=1, sticky=E)
        self.display_closed.grid(row=3, column=1, sticky=E)

        #self.paint_scenario(self.gs.search_yieldie())

    def paint_scenario(self):
        self.set_map()
        gs_gen = self.gs.search_yieldie()
        start = time.time()

        for solution in gs_gen:
            if solution['solved']:
                print("SOLVED")
                self.display_time.configure(text="%.2f" % (time.time() - start))
                break

            print("Solving!")
            y = -1
            for i in range(self.nono.total_rows):
                domain = solution['node'].get_domain(i)[0]
                x = -1
                y += 1
                for item in domain[1]:
                    x += 1
                    if not item:
                        self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill="white", tags='rectangle')
                    elif item:
                        self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill="blue", tags='rectangle')

    def set_map(self, scenario=None):
        print("Changed map")
        self.canvas.delete('all')
        self.nono.set_scenario('modul3/scenarioes/' + self.selected_scenario.get())
        self.gs = GraphSearch(self.nono, Agenda)




    '''
    def load_scenario(self):
        file = filedialog.askopenfilename(parent=self, filetypes=[('Text Files', '.txt')],
                                          title='Select a scenario file')

        file = file.split('/')[-1]
        self.paint_scenario(file)
    '''




