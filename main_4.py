from tkinter import Tk
from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax_top
import time
import numpy as np

if __name__ == '__main__':
    g = _2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial

    root = Tk()
    app = GameWindow(master=root)
    score = 0

    t1 = time.time()
    timer = ""
    for i in range(10):
        state = g.initial
        actions = list(g.actions(state))
        while actions:
            timer = '%.2f' % (time.time() - t1)
            app.update_view(state, score, timer)
            prev = state
            _, state = expectimax_top(g, state)

            prev_diff = np.setdiff1d(prev.reshape(-1), state.reshape(-1))
            if prev_diff.size:
                for i in prev_diff:
                    score += 1 << i
            state = g.adv_move(state)

            actions = list(g.actions(state))
        print(state, timer)

    app.update_view(state, score, 0)
    app.game_over_screen()
    time.sleep(3)

