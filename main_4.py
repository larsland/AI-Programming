from tkinter import Tk
from modul4.gui import GameWindow

if __name__ == '__main__':
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