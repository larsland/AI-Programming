# from tkinter import Tk
# from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax_top
import time
import numpy as np


def pretty_print_4x4_np(state):
    board = np.copy(state)
    for (i, j), _ in np.ndenumerate(state):
        board[i, j] = 1 << state[i, j] if state[i, j] != 0 else 0
    print(board)


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
    '''

    t1 = time.time()
    for i in range(1):
        state = g.initial
        actions = list(g.actions(state, True))
        while actions:
            _, state = expectimax_top(g, state, depth=4)
            pretty_print_4x4_np(state)
            state = g.adv_move(state)
            # print('a', state)
            actions = list(g.actions(state, True))
        print(state)

    print(time.time() - t1)
