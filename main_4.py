from tkinter import Tk
import time
from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax
import numpy as np

if __name__ == '__main__':

    root = Tk()
    app = GameWindow(master=root)

    g = _2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial

    actions = list(g.actions(state, True))
    score = 0
    while actions:
        app.update_view(state, score)

        prev = state
        _, state = expectimax(g, state)
        prev_diff = np.setdiff1d(prev.reshape(-1), state.reshape(-1))
        if prev_diff.size:
            for i in prev_diff:
                score += 1 << i

        state = g.adv_move(state)
        actions = list(g.actions(state, True))

    app.update_view(state, score)

    app.game_over_screen()
    time.sleep(3)
