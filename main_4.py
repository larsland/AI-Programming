from tkinter import Tk
from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax


import sys
if __name__ == '__main__':

    root = Tk()
    app = GameWindow(master=root)
    # sys.setrecursionlimit(10000)

    g = _2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial

    actions = list(g.actions(state, True))
    while actions:
        app.update_view(state)
        _, state = expectimax(g, state)
        state = g.adv_move(state)
        actions = list(g.actions(state, True))

    app2 = GameWindow(state, master=root)
    app2.mainloop()
