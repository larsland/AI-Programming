import random
from tkinter import *
from tkinter import font

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


class Tile:
    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return str(self.value)


class GameWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.font = font.Font(master, family="Verdana", size=40, weight="bold")
        self.score_font = font.Font(master, family="Verdana", size=20)
        self.master.title('2048')
        self.grid()
        self.board = [[Tile() for x in range(4)] for x in range(4)]
        self.master.bind("<KeyPress>", self.onKeyPress)
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

        self.add_random_tile()
        self.add_random_tile()

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

    def move(self, direction):
        if self.check_if_lost():
            self.game_over_screen()
        merged = []
        moved = False
        lines = self.rotate(self.board, direction+1)
        for line in lines:
            while len(line) and line[-1].value == 0:
                line.pop(-1)
            i = len(line)-1
            while i >= 0:
                if line[i].value == 0:
                    moved = True
                    line.pop(i)
                i -= 1
            i = 0
            while i < len(line)-1:
                if line[i].value == line[i+1].value and not (line[i] in merged or line[i+1] in merged):
                    moved = True
                    line[i] = Tile(line[i].value + 1)
                    self.score += 1 * (2**line[i].value)
                    merged.append(line[i])
                    line.pop(i+1)
                else:
                    i += 1
            while len(line) < len(self.board):
                line.append(Tile())

        self.board = self.rotate(lines, 0-(direction+1))
        self.next_step(moved)

    def rotate(self, l, num):
        num %= 4
        s = len(l)-1
        l2 = []
        if num == 0:
            l2 = l
        elif num == 1:
            l2 = [[None for i in j] for j in l]
            for y in range(len(l)):
                for x in range(len(l[y])):
                    l2[x][s-y] = l[y][x]
        elif num == 2:
            l2 = l
            l2.reverse()
            for i in l:
                i.reverse()
        elif num == 3:
            l2 = [[None for i in j] for j in l]
            for y in range(len(l)):
                for x in range(len(l[y])):
                    l2[y][x] = l[x][s-y]
        return l2

    def next_step(self, moved):
        if moved:
            self.add_random_tile()
        self.update_view()

    def add_random_tile(self):
        empty_spots = []
        for i in range(0, 4):
            for j in range(0, 4):
                if self.board[i][j].value == 0:
                    empty_spots.append((i, j))
        if empty_spots:
            tile = random.choice(empty_spots)
            n = self.distributed_tile()
            self.board[tile[0]][tile[1]].value = n

    def distributed_tile(self):
        return 1 if random.randint(0, 100) < 90 else 2

    def onKeyPress(self, event):
        if event.keysym == 'Left':
            self.move(3)
        elif event.keysym == 'Up':
            self.move(2)
        elif event.keysym == 'Right':
            self.move(1)
        elif event.keysym == 'Down':
            self.move(0)

    def check_if_lost(self):
        s = len(self.board)-1
        b = True
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                val = self.board[i][j].value
                if val == 0:
                    b = False
                if i > 0 and self.board[i-1][j].value == val:
                    b = False
                if j > 0 and self.board[i][j-1].value == val:
                    b = False
                if i < s and self.board[i+1][j].value == val:
                    b = False
                if j < s and self.board[i][j+1].value == val:
                    b = False
        return b
