from tkinter import Tk
from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax
import numpy as np

import sys
if __name__ == '__main__':

    root = Tk()
    app = GameWindow(master=root)
    sys.setrecursionlimit(10000)

    g = _2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial

    '''
    print(state)

    _, state = expectimax(g, state)
    print('p: \n', state)

    state = g.adv_move(state)
    print('a: \n', state)

    _, state = expectimax(g, state)
    print('p: \n', state)

    state = g.adv_move(state)
    print('a: \n', state)

    _, state = expectimax(g, state)
    print('p: \n', state)

    '''



    actions = list(g.actions(state, True))
    while actions:
        _, state = expectimax(g, state)
        print('p', state)
        state = g.adv_move(state)
        print('a', state)
        actions = list(g.actions(state, True))
        app.update_view(state)


    """
    root = Tk()
    app = GameWindow(master=root)
    '''
    writer = app.ThreaderAnimator
    game = _2048
    alg = minimax
    '''
    app.mainloop()
    '''
    writer.write(alg(game))
    '''
    """
