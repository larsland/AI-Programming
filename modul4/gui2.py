import random, colorsys
from tkinter import *

class Game:
    def __init__(self, master=None):
        self.grid = [[Tile() for i in range(4)] for j in range(4)]
        self.addRandomTile()
        self.addRandomTile()

    def addRandomTile(self):
        availableTiles = self.getAvailableTiles()
        findTile = self.findTile(random.choice(availableTiles))
        self.grid[findTile[0]][findTile[1]] = Tile(2)

    def getAvailableTiles(self):
        ret = []
        for i in self.grid:
            for j in i:
                if j.value == 0:
                    ret.append(j)
        return ret

    def findTile(self, tile):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == tile:
                    return i, j

    def move(self, direction):
        merged = []
        moved = False
        lines = rotate(self.grid, direction+1)
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
                    line[i] = Tile(line[i].value*2)
                    merged.append(line[i])
                    line.pop(i+1)
                else:
                    i += 1
            while len(line) < len(self.grid):
                line.append(Tile())
        for line in lines:
            if not len(lines):
                line = [Tile() for i in self.grid]
        self.grid = rotate(lines, 0-(direction+1))
        if moved:
            self.addRandomTile()

    def get_values(self):
        ret = []
        for i in self.grid:
            for j in i:
                ret.append(j)
        return ret

class Tile:
    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return str(self.value)


def rotate(l, num):
    num = num % 4
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


def onKeyPress(event):
    global g
    global b
    for i in b:
        for j in i:
            j.destroy()
    if event.keysym == 'Left':
        g.move(3)
    elif event.keysym == 'Up':
        g.move(2)
    elif event.keysym == 'Right':
        g.move(1)
    elif event.keysym == 'Down':
        g.move(0)
    makeButtons(g)


def makeButtons(g):
    global b
    for i in range(len(g.grid)):
        for j in range(len(g.grid[i])):
            if g.grid[i][j].value:
                b[i][j] = Button(root, text=str(g.grid[i][j].value), bg=findColors(g.grid[i][j].value)[0], fg=findColors(g.grid[i][j].value)[1])
            else:
                b[i][j] = Button(root, text='')
            b[i][j].config(width=max(len(str(i)) for i in g.get_values()))
            b[i][j].grid(row=i, column=j)


def findColors(num):
    if (num != 0 and ((num & (num - 1)) == 0)):
        bi = bin(num)
        po = len(bi)
        hue = 30.0 * po
        rgb = colorsys.hls_to_rgb(hue/256.0, 0.5, 0.5)
        rgb = [str(hex(int(256*x)))[2:3] for x in rgb]
        return "#" + str(rgb[0]) + str(rgb[1]) + str(rgb[2]), "#FFFFFF"
    else:
        return "#000000", "#FFFFFF"

g = Game(4)
b = [[None for i in j] for j in g.grid]

root = Tk()
root.bind('<KeyPress>', onKeyPress)

makeButtons(g)

root.mainloop()

'''
if __name__ == '__main__':
    root = Tk()
    app = Game(master=root)
    app.mainloop()
'''