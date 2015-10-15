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
        self.board = [[0 for x in range(4)] for x in range(4)]

        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)

        self.grid_cells = []
        self.init_grid()
        self.update_view()


    def init_grid(self):
        background = Frame(self, bg = BACKGROUND_COLOR_GAME, width = SIZE, height = SIZE )
        background.grid()

        for i in range(GRID_LEN):
            # Loop rows
            grid_row = []

            for j in range(GRID_LEN):
                # Loop columns
                cell = Frame(background, bg = BACKGROUND_COLOR_CELL_EMPTY, width = SIZE/GRID_LEN, height = SIZE/GRID_LEN)

                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

        self.add_init_tiles()


    def update_view(self):
        print("UPDATING")
        for i in range( GRID_LEN ):
            for j in range( GRID_LEN ):
                digit = self.board[i][j]
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

    def move_up(self, event):
        print("MOVED UP")
        for i in range(0, 4):
            for j in range(0, 4):
                tile = self.board[i][j]
                if tile != 0:
                    if i-1 <= -1:
                        pass
                    else:
                        if self.board[i-1][j] == tile:
                            self.board[i-1][j] += 1
                        elif self.board[i-1][j] == 0:
                            self.board[i-1][j] = tile
                        else:
                            pass

                        if i+1 >= 4:
                            self.board[i][j] = 0
                        else:
                            self.board[i][j] = self.board[i+1][j]
        self.next_step()

    def move_down(self, event):
        print("MOVED DOWN")
        for i in range(0, 4):
            for j in range(0, 4):
                tile = self.board[i][j]
                if tile != 0:
                    if i+1 >= 4:
                        pass
                    else:
                        if self.board[i+1][j] == tile:
                            self.board[i+1][j] += 1
                        elif self.board[i+1][j] == 0:
                            self.board[i+1][j] = tile
                        else:
                            pass

                        if i-1 <= -1:
                            self.board[i][j] = 0
                        else:
                            self.board[i][j] = self.board[i-1][j]
        self.next_step()

    def move_left(self, event):
        print("MOVED LEFT")
        for i in range(0, 4):
            for j in range(0, 4):
                tile = self.board[i][j]
                if tile != 0:
                    if j-1 <= -1:
                        pass
                    else:
                        if self.board[i][j-1] == tile:
                            self.board[i][j-1] += 1
                        elif self.board[i][j-1] == 0:
                            self.board[i][j-1] = tile
                        else:
                            pass

                        if j+1 >= 4:
                            self.board[i][j] = 0
                        else:
                            self.board[i][j] = self.board[i][j+1]
        self.next_step()

    def move_right(self, event):
        print("MOVED RIGHT")
        for i in range(0, 4):
            for j in range(0, 4):
                tile = self.board[i][j]
                if tile != 0:
                    if j+1 >= 4:
                        pass
                    else:
                        if self.board[i][j+1] == tile:
                            self.board[i][j+1] += 1
                        elif self.board[i][j+1] == 0:
                            self.board[i][j+1] = tile
                        else:
                            pass

                        if j-1 <= -1:
                            self.board[i][j] = 0
                        else:
                            self.board[i][j] = self.board[i][j-1]
        self.next_step()

    def next_step(self):
        self.update_view()
        self.add_random_tile()

    def add_init_tiles(self):
        tile_1 = random.sample(range(0, 4), 2)
        tile_2 = random.sample(range(0, 4), 2)

        self.board[tile_1[0]][tile_1[1]] = 1
        self.board[tile_2[0]][tile_2[1]] = 1

        self.update_view()

    def add_random_tile(self):
        empty_spots = []
        for i in range(0, 4):
            for j in range(0, 4):
                if self.board[i][j] == 0:
                    empty_spots.append((i, j))

        tile = random.choice(empty_spots)

        self.board[tile[0]][tile[1]] = 1

    def game_won(self):
        return False

    def game_lost(self):
        return False

if __name__ == '__main__':
    root = Tk()
    app = GameWindow(master=root)
    app.mainloop()
