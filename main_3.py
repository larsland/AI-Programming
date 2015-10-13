from tkinter import Tk
from modul3.gui import Gui
from modul3.nonograms_problem import NonogramProblem
from algorithms.search import GraphSearch, Agenda

if __name__ == '__main__':

    root = Tk()
    app = Gui(master=root)
    app.mainloop()

