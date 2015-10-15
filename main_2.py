from tkinter import Tk
from modul2.gui import Gui

if __name__ == '__main__':
    root = Tk()
    app = Gui(master=root)
    # root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    app.mainloop()