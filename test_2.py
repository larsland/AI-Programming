from modul2.VC import VCProblem
from modul2.problem import GraphSearch, Agenda
import time


if __name__ == '__main__':

    s = time.time()
    VC = VCProblem()
    s2 = time.time()
    GS = GraphSearch(problem=VC, frontier=Agenda)
    s3 = time.time()
    path = GS.search()
    s4 = time.time()
    print("path", path)