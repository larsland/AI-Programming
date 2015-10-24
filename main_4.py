from tkinter import Tk
from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax
import numpy as np
import time

import sys
if __name__ == '__main__':


    g = _2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial
    print(state)
    '''
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

    times = []
    t1 = time.time()
    for i in range(100):
        state = g.initial
        actions = list(g.actions(state, True))
        while actions:
            _, state = expectimax(g, state)
            # print('p', state)
            state = g.adv_move(state)
            # print('a', state)
            actions = list(g.actions(state, True))

    print(time.time() - t1)

    g.adv_move = g.adv_move2
    t1 = time.time()
    for i in range(100):
        state = g.initial
        actions = list(g.actions(state, True))
        while actions:
            _, state = expectimax(g, state)
            # print('p', state)
            state = g.adv_move(state)
            # print('a', state)
            actions = list(g.actions(state, True))

    print(time.time() - t1)
