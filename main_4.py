from tkinter import Tk
from modul4.gui import GameWindow
from modul4.gamelogic import _2048
from modul4.adversial import expectimax
from algorithms.utils import Bunch
import numpy as np
if __name__ == '__main__':
    g = _2048()
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