import math
import numpy as np
import json


def read_2048_file(file_path):
    data = []
    with open(file_path) as mini:
        i = 0
        block = {}
        block['board'] = []
        for line in mini:
            if line.find('Move') == 0:
                i += 1
                if block != {'board': []}:
                    block['board'] = np.array(block['board']).flatten().tolist()
                    yield block
                    block = {}
                block['board'] = []
                block['score'] = line.split('=')[1].rstrip('\r\n')
            else:
                # print(line)
                row = line.split(' ')
                flat_board = []
                if len(row) > 1:
                    for item in row:
                        item = item.rstrip('\r\n')
                        if item != '':
                            item = int(item)
                            if item == 0:
                                flat_board.append(0)
                            else:
                                flat_board.append(int(math.log2(int(item))))
                    block['board'].append(flat_board)
                else:
                    item = row[0].rstrip('\r\n')
                    if item != '':
                        block['move'] = int(item)

        block['board'] = np.array(block['board']).flatten().tolist()
        yield block


def write_training_data(in_file, out_file):
    errors = 0
    with open(out_file, 'w') as testorama:
        for block in read_2048_file(in_file):
            try:
                line = '%s, %i, %s\n' % (block['board'], block['move'], block['score'])
                testorama.write(line)
            except KeyError:
                errors += 1
                pass

        print("experienced %s errors" % errors)


def sick_if_bro(x):
    if x == [1, 0, 0, 0]:
        return 0
    elif x == [0, 1, 0, 0]:
        return 1
    elif x == [0, 0, 1, 0]:
        return 2
    elif x == [0, 0, 0, 1]:
        return 3


def sick_log2_bro(flat_board):
    result = []
    for i in range(len(flat_board)):
        if flat_board[i] > 0:
            result.append(int(math.log2(flat_board[i])))
        else:
            result.append(0)
    return result


def interpret_team_hereforbeer(in_file, out_file):
    with open(out_file, 'w+') as out:
        with open(in_file) as data_file:
            data = json.load(data_file)
            for object in data:
                output_str = str(sick_log2_bro(eval(object))) + ', ' + str(sick_if_bro(data[object])) + ', 0\n'
                out.write(output_str)



if __name__ == '__main__':
    interpret_team_hereforbeer('myfile.txt', 'hereforbeer_training.txt')
    # write_training_data('data2.txt', 'new_training_set.txt')
