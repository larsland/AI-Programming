from __future__ import print_function
from Tkinter import *


class Astar_program(Frame):

	def __init__(self, master = None):
		Frame.__init__(self, master)
		self.master.title("A* Search")
		self.pack()
		self.create_gui()


	def create_gui(self):
		# Creating the canvas where the grid is drawn
		canvas = Canvas(self, width=500, height=500)
		self.create_grid(canvas, "map1.txt")

		# Variable for the current mode, and setting a default
		selected_mode = StringVar(self)
		selected_mode.set("Best-first mode")

		# Variable for the current map, and setting a default
		selected_map = StringVar(self)
		selected_map.set("map1.txt")
		
		# Creating the menus and buttons
		mode_menu = OptionMenu(self, selected_mode, "Best-first mode", "Depth-first mode", "Breadth-first mode", command = lambda mode:print(mode))
		map_menu = OptionMenu(self, selected_map, "map1.txt", "map2.txt", "map3.txt", "map4.txt", "map5.txt", "map6.txt", command = lambda map:self.create_grid(canvas, map))
		start_btn = Button(self, text="Start", fg="green", command = self.start_program)
		exit_btn = Button(self, text="Exit", fg="red", command = self.quit)
		
		# Placing components in a grid
		mode_menu.grid(row = 0, column = 0)
		map_menu.grid(row = 0, column = 1)
		start_btn.grid(row = 0, column = 2)
		exit_btn.grid(row = 0, column = 3)
		canvas.grid(row = 1, column = 0, columnspan = 4)

	def create_grid(self, canvas, map):

		mapstring = ""
		fo = open(map, "rw+")
		for line in fo.readlines():
			for c in line:
				#if c == '\n':
				#	mapstring += 'n'
				mapstring += c

		x0_counter = 0
		y0_counter = 0
		x1_counter = 50
		y1_counter = 50

		for c in mapstring:
			if c == '_':
				canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="white")
			elif c == '#':
				canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="black")
			elif c == 'A':
				canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="green")
			elif c == 'B':
				canvas.create_rectangle(x0_counter, y0_counter, x1_counter, y1_counter, fill="red")

			x0_counter += 50
			x1_counter += 50

			if c == '\n':
				x0_counter = 0
				y0_counter += 50
				x1_counter = 50
				y1_counter += 50

	# Method for starting the application with the chosen algorithm
	def start_program(self):
		print ("START")


def main():
	root = Tk()
	app = Astar_program(master=root)
	app.mainloop()
	root.destroy

main()