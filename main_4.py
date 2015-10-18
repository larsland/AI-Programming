from tkinter import Tk
from modul4.gui import GameWindow

if __name__ == '__main__':
    root = Tk()
    app = GameWindow(master=root)
    app.mainloop()