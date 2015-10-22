import random
from tkinter import *
from tkinter import font
from modul4.gamelogic import _2048, Tile
from algorithms.utils import Bunch

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
        self.board = [[Tile() for x in range(4)] for x in range(4)]
        self.master.bind("<KeyPress>", self.on_key_press)
        self.grid_cells = []
        self.score = 0
        self.score_board = None
        self.init_grid()
        self.update_view()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        self.score_board = Label(self, text="0", font=self.score_font)
        score_board_label = Label(self, text="Score:", font=self.score_font)
        score_board_label.grid(row=0, column=0, sticky=E)
        self.score_board.grid(row=0, column=1, sticky=W)
        background.grid(row=1, column=0, columnspan=2)

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

        self.board = self.game.adv_move(Bunch(board=self.board))
        self.board = self.game.adv_move(Bunch(board=self.board))


    def update_view(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                digit = self.board[i][j].value
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

        self.score_board.configure(text=self.score)
        self.update_idletasks()

    def game_over_screen(self):
        screen = Frame(self, bg="gray", width=SIZE, height=SIZE)
        screen.grid(row=1, column=0, columnspan=2, sticky=N+W+E+S)
        message = Label(screen, bg="gray", font=self.font, text="Game Over!")
        message.grid(row=1, column=0, sticky=E+S+W+N, padx=170, pady=150)
        btn_exit = Button(screen, text="OK", bg="#E6E6E6", font=self.font, padx=50, command=self.quit)
        btn_exit.grid(row=2, column=0)


    def on_key_press(self, event):
        state = Bunch(to_move=0, utility=0, board=self.board)
        legal = self.game.legal_moves(state)
        print(legal)
        if not legal:
            self.game_over_screen()
        else:
            if event.keysym == 'Left' and 3 in legal:
                state = self.game.make_move(Bunch(to_move=0, utility=0, board=self.board), 3)
                self.board = state.board
                self.update_view()

                state = self.game.make_move(Bunch(to_move=1, utility=0, board=self.board))
                self.board = state.board
                self.update_view()
            elif event.keysym == 'Up' and 2 in legal:
                state = self.game.make_move(Bunch(to_move=0, utility=0, board=self.board), 2)
                self.board = state.board
                self.update_view()

                state = self.game.make_move(Bunch(to_move=1, utility=0, board=self.board))
                self.board = state.board
                self.update_view()
            elif event.keysym == 'Right' and 1 in legal:
                state = self.game.make_move(Bunch(to_move=0, utility=0, board=self.board), 1)
                self.board = state.board
                self.update_view()

                state = self.game.make_move(Bunch(to_move=1, utility=0, board=self.board))
                self.board = state.board
                self.update_view()
            elif event.keysym == 'Down' and 0 in legal:
                state = self.game.make_move(Bunch(to_move=0, utility=0, board=self.board), 0)
                self.board = state.board
                self.update_view()

                state = self.game.make_move(Bunch(to_move=1, utility=0, board=self.board))
                self.board = state.board
                self.update_view()


