from tkinter import Tk
from modul2.gui import Gui

if __name__ == '__main__':
    root = Tk()
    app = Gui(master=root)
    app.mainloop()