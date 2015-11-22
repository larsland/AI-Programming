import math
from random import randint
from tkinter import Tk
import numpy as np
import time
from modul6.ann import ANN
import theano.tensor.nnet as Tann
from modul4 import gamelogic as game
from modul4.gui import GameWindow
from modul4.adversial import *
from modul5.utils import rectify
from modul6.ai2048demo import welch


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

tile_list = []


def add_highest_tile(state):
    highest_tile = max(np.asarray(state).flatten().tolist())
    tile_list.append(2**highest_tile)


def get_avarage_tile():
    return sum(tile_list)/float(len(tile_list))

if __name__ == '__main__':
    states, labels, scores = [], [], []
    with open('modul6/training_data.txt') as training_file:
        for line in training_file:
            data = eval(line)
            states.append(np.asarray(data[0]))
            labels.append(data[1])
            scores.append(data[2])
    ann = ANN(states, labels, scores, [625], [Tann.softplus, Tann.softplus, Tann.softmax], 0.005, 20, 1, 5, 'mean')
    ann.run()

    g = game._2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial

    root = Tk()
    app = GameWindow(master=root)
    score = 0

    t1 = time.time()
    timer = ""

    sic_dic = {0: 2,
               1: 0,
               2: 3,
               3: 1}

    actions = list(g.actions(state))

    for i in range(50):
        state = g.initial
        actions = list(g.actions(state))
        while actions:
            move = randint(0, 3)
            state = g.my_move(state, sic_dic[move])
            print(state)
            state = g.adv_move(state)
            print(state)
            actions = list(g.actions(state))

        add_highest_tile(state)
    print(get_avarage_tile())
    time.sleep(3)








