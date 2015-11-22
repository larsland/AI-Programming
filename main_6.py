from modul5.ann import ANN
import theano.tensor.nnet as Tann
from modul5.basics.mnist_basics import *

from modul5.utils import rectify
import copy
from modul5.ann import *
import math
import numpy as np


def read_2048_file(file_path):
    data = []
    with open('modul6/mini.txt') as mini:
        block = {}
        block['board'] = []
        for line in mini:
            if line.find('Move') == 0:
                if block != {'board': []}:
                    block['board'] = np.array(block['board']).flatten()
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

        block['board'] = np.array(block['board']).flatten()
        yield block


if __name__ == '__main__':

    #ann2 = ANN(cases, test_cases, [535], [Tann.softplus, Tann.softplus, Tann.softmax], 0.001, 100, 1, 10, 'mean')
    for block in read_2048_file('modul6/mini.txt'):
        print(block)