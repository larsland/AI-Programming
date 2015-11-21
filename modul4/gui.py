from tkinter import *
from tkinter import font
from modul4.gamelogic import _2048

GRID_LEN = 4
GRID_PADDING = 10
SIZE = 500

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_CELL_FALLBACK = "#404040"
BACKGROUND_COLOR_DICT = {
    1: '#E9DED0',
    2: '#E8DAB9',
    3: '#EAA35D',
    4: '#EC8348',
    5: '#EC6B47',
    6: '#EB4925',
    7: '#E6C84F',
    8: '#E6C53A',
    9: '#edc850',
    10: '#edc53f',
    11: '#FFAE00'
}


class GameWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.font = font.Font(master, family="Verdana", size=40, weight="bold")
        self.score_font = font.Font(master, family="Verdana", size=20)
        self.master.title('2048')
        self.grid()
        self.game = _2048()
        self.grid_cells = []
        self.score = 0
        self.score_board = None
        self.timer = None
        self.init_grid()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        self.score_board = Label(self, text="0", font=self.score_font)
        score_board_label = Label(self, text="Score:", font=self.score_font)
        score_board_label.grid(row=0, column=0, sticky=E)
        self.score_board.grid(row=0, column=1, sticky=W)
        background.grid(row=1, column=0, columnspan=3)
        self.timer = Label(self, text=0, font=self.score_font)
        self.timer.grid(row=0, column=2, sticky=E)

        for i in range(GRID_LEN):
            # Loop rows
            grid_row = []

            for j in range(GRID_LEN):
                # Loop columns
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)

                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=self.font, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_view(self, state, score, time):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                digit = state[i, j]
                if digit == 0:
                    self.grid_cells[i][j].configure(
                        text="",
                        bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    foreground_color = '#F7F4EE' if digit > 2 else '#635B51'
                    number = 1 << digit  # the human friendly representation

                    self.grid_cells[i][j].configure(
                        text=str(1 << digit),
                        bg=BACKGROUND_COLOR_DICT.get(digit, BACKGROUND_COLOR_CELL_FALLBACK),
                        fg=foreground_color)

        self.score_board.configure(text=score)
        self.timer.configure(text=time)
        self.update_idletasks()

    def game_over_screen(self):
        print("Game Over!")
        screen = Frame(self,  width=50, height=20)
        screen.grid(row=1, column=0, columnspan=2)
        message = Label(screen, font=self.font, text="Game Over!")
        message.grid(row=1, column=0, sticky=E+S+W+N)

        self.update_idletasks()

