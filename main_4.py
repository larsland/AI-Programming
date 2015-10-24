from tkinter import Tk
from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax
from algorithms.utils import Bunch
import numpy as np
if __name__ == '__main__':

    g = _2048()
    g.initial = g.adv_move(g.initial)
    state = g.initial
    actions = list(g.actions(state, True))
    while actions:
        alpha = -float('Inf')
        for t_alpha, t_state in actions:

            t_alpha, t_state = expectimax(g, t_state)
            print('t_alpha: %s vs alpha: %s \n t_state: \n %s \n vs  \n state: \n %s ' % (t_alpha, alpha, t_state, state))

            if alpha > t_alpha:
                alpha = t_alpha
                state = t_state

        print("State: \n %s" % state)
        actions = list(g.actions(state, True))

    print(expectimax(g, g.initial))
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
