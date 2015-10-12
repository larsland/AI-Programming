from tkinter import Tk
from modul3.gui import Gui
from modul3.nonograms_problem import NonogramProblem
from algorithms.search import GraphSearch, Agenda
from pprint import PrettyPrinter

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)
    Nono = NonogramProblem()
    Nono.set_scenario()
    gs = GraphSearch(Nono, Agenda)

    root = Tk()
    app = Gui(Nono, gs, master=root)
    app.mainloop()

