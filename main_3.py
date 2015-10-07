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


init()