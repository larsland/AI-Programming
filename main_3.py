from tkinter import Tk
from modul3.gui import Gui


class Variable:
    def __init__(self, type, state, index):
        self.type = type
        self.index = index
        self.state = state
        self.domain = []

    def __repr__(self):
        return "ID: " + str(self.index) + \
               " Type: " + str(self.type) +  \
               " State: " + str(self.state) + \
               " Domain: " + str(self.domain)


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


def create_vars(matrix):
    vars = []
    for row in range(len(matrix)):
        vars.append(Variable("row", matrix[row], row))
    for i in range(len(matrix[0])):
        vars.append(Variable("col", [row[i] for row in matrix], len(matrix) + i))

    return vars


def printer(row_specs, col_specs, matrix, num_cols, num_rows):
    for line in range(len(matrix)):
        print(matrix[line])

    print("NUMBER OF COLUMNS: " + str(num_cols))
    print("NUMBER OF ROWS: " + str(num_rows))
    print("ROW SPECS: ")
    print(row_specs)
    print("COL SPECS: ")
    print(col_specs)


def init():
    scenario = get_scenario()

    num_cols = int([i for i in scenario[0].split()][0])
    num_rows = int([i for i in scenario[0].split()][1])

    row_specs = get_row_specs(scenario, num_rows)
    col_specs = get_col_specs(scenario, num_rows)

    matrix = [['0' for x in range(num_cols)] for x in range(num_rows)]
    matrix[0][0] = 'X'
    matrix[6][0] = 'X'

    vars = create_vars(matrix)

    for i in range(0, len(row_specs)):
        vars[i].domain = row_specs[i]

    counter = 0
    for i in range(len(row_specs), len(vars)):
        vars[i].domain = col_specs[counter]
        counter += 1

    for i in range(0, len(vars)):
        print(vars[i])



    root = Tk()
    app = Gui(matrix, master=root)
    app.mainloop()


init()
