from tkinter import Tk
from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax_top, get_dynamic_depth
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

    root = Tk()
    app = GameWindow(master=root)
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
    success = 0
    for i in range(3):
        state = g.initial
        actions = list(g.actions(state))
        while actions:
            app.update_view(state)
            _, state = expectimax_top(g, state)
            state = g.adv_move(state)
            # print('a', state)
            actions = list(g.actions(state))
            # pretty_print_4x4_np(state)
        if state.max() >= 11:
            print("woop woop!")
            success += 1
        print(time.time() - t1)
        print("success rate: %s" % (success / 3.0))

    app.update_view(state)
    app.game_over_screen()
    time.sleep(3)

    print(time.time() - t1)
    print("success rate: %s" % (success / 1.0))

