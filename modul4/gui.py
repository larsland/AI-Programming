import random
from tkinter import *

GRID_LEN              = 4
GRID_PADDING          = 10
SIZE                  = 500

BACKGROUND_COLOR_GAME       = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
FONT                        = ("Verdana", 40, "bold")
BACKGROUND_COLOR_DICT       = {
                                1  : '#eee4da',
                                2  : '#ede0c8',
                                3  : '#f2b179',
                                4  : '#f59563',
                                5  : '#f67c5f',
                                6  : '#f65e3b',
                                7  : '#edcf72',
                                8  : '#edcc61',
                                9  : '#edc850',
                                10 : '#edc53f',
                                11 : '#FFAE00',
                                12 : '#FFAE00',
                                13 : '#FFAE00',
                                14 : '#FFAE00',
                                15 : '#FFAE00',
                                16 : '#FFAE00'
                            }

class GameWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('2048')
        self.grid()
        self.tiles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.grid_cells = []
        self.init_grid()
        self.update_view(self.tiles)
    #end

    def init_grid(self):
        background = Frame(self, bg = BACKGROUND_COLOR_GAME, width = SIZE, height = SIZE )
        background.grid()

        for i in range(GRID_LEN):
            # Loop rows
            grid_row = []

            for j in range(GRID_LEN):
                # Loop columns
                cell = Frame(
                            background,
                            bg     = BACKGROUND_COLOR_CELL_EMPTY,
                            width  = SIZE/GRID_LEN,
                            height = SIZE/GRID_LEN)

                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

        self.add_init_tiles()
        print(self.grid_cells)
        self.play()
    #end

    def update_view(self, board ):
        for i in range( GRID_LEN ):
            for j in range( GRID_LEN ):
                digit = board[i*4+j]
                if digit == 0:
                    self.grid_cells[i][j].configure(
                                                text = "",
                                                bg   = BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    foreground_color = '#f9f6f2' if digit > 2 else '#776e65'
                    number = 1 << digit # the human friendly representation

                    self.grid_cells[i][j].configure(
                                                text = str( 1 << digit ),
                                                bg   = BACKGROUND_COLOR_DICT[ digit ],
                                                fg   = foreground_color )
        self.update_idletasks()

    def move(self, direction):
        if direction == 'up':
            print("Moving UP")

        elif direction == 'down':
            print("Moving DOWN")

        elif direction == 'left':
            print("Moving LEFT")

        elif direction == 'right':
            print("Moving RIGHT")

        



    def play(self):
        while True:
            key = input("Key: ")
            if key == 'q':
                break
            elif key == '\x1b[A':
                self.move('up')
            elif key == '\x1b[B':
                self.move('down')
            elif key == '\x1b[D':
                self.move('left')
            elif key == '\x1b[C':
                self.move('right')

            if self.game_won():
                print("Congratulations, you have reached a tile with 2048")

            if self.game_lost():
                print("Game over")

    def game_won(self):
        return False

    def game_lost(self):
        return False

    def add_init_tiles(self):
        indexes = random.sample(range(0, 15), 2)

        self.tiles[indexes[0]] = 1
        self.tiles[indexes[1]] = 1

        self.update_view(self.tiles)


if __name__ == '__main__':
    root = Tk()
    app = GameWindow(master=root)
    app.mainloop()
