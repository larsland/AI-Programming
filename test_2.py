from tkinter import Tk
from modul2.gui import Gui
from modul2.vcgraph_problem import VertexColoringProblem
from modul2.search import GraphSearch, Agenda
import time


def ms_to_s(ms):
    s = ms / 1000.0
    return s

if __name__ == '__main__':
    """
    t1 = time.time()
    VC = VertexColoringProblem()
    VC.set_graph(graph='graph3.txt', dom_size=4)
    t2 = time.time()
    GS = GraphSearch(problem=VC, frontier=Agenda)
    t3 = time.time()
    VCNodes, found = GS.search()
    t4 = time.time()
    # print("Solved: ", path)
    print("Times: VC_init: %s, GraphSearch_init: %s, search: %s" % (t2-t1, t3-t2, t4-t3))

    i=0
    for VCGACNode in VCNodes:
        print('-----------------------------------', i)
        i+=1
        print(VCGACNode.node_domain_map)
    """
    root = Tk()
    app = Gui(master=root)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    app.mainloop()