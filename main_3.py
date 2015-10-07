from tkinter import Tk
from modul3.gui import Gui

def get_scenario():
    input_scenario = input("Select scenario (0-6): ")
    input_scenario = "scenario" + str(input_scenario) + ".txt"
    scenario= open('modul3/' + input_scenario, 'r').read().splitlines()
    return scenario


def get_row_specs(scenario, num_rows):
    row_specs = []
    for line in range(1, num_rows + 1):
        row_specs.append([i for i in scenario[line].split()])
    return row_specs


def get_col_specs(scenario, num_rows):
    col_specs = []
    for line in range(num_rows + 1, len(scenario)):
        col_specs.append([i for i in scenario[line].split()])
    return col_specs


def init():
    scenario = get_scenario()

    num_cols = int([i for i in scenario[0].split()][0])
    num_rows = int([i for i in scenario[0].split()][1])

    row_specs = get_row_specs(scenario, num_rows)
    col_specs = get_col_specs(scenario, num_rows)

    matrix = [['0' for x in range(num_cols)] for x in range(num_rows)]

    for line in range(len(matrix)):
        print(matrix[line])

    print("NUMBER OF COLUMNS: " + str(num_cols))
    print("NUMBER OF ROWS: " + str(num_rows))
    print("ROW SPECS: ")
    print(row_specs)
    print("COL SPECS: ")
    print(col_specs)

    matrix[0][0] = 'X'

    root = Tk()
    app = Gui(matrix, master=root)
    app.mainloop()




init()