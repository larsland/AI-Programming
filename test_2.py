from tkinter import Tk
from modul2.gui import Gui
from modul2.vcgraph_problem import VCProblem
from modul2.search import GraphSearch, Agenda
import time


def ms_to_s(ms):
    s = ms / 1000.0
    return s

if __name__ == '__main__':
    t1 = time.time()
    VC = VCProblem()
    t2 = time.time()
    GS = GraphSearch(problem=VC, frontier=Agenda)
    t3 = time.time()
    path = GS.search()
    t4 = time.time()
    # print("Solved: ", path)
    print("Times: VC_init: %s, GraphSearch_init: %s, search: %s" % (t2-t1, t3-t2, t4-t3))

    root = Tk()
    app = Gui(VC, master=root)
    app.mainloop()

