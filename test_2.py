from modul2.VC import VCProblem
from modul2.problem import GraphSearch, Agenda
import time


if __name__ == '__main__':
    VC = VCProblem()
    GS = GraphSearch(problem=VC, frontier=Agenda)
    path = GS.search()
    print("Solved: ", path)