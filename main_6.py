import math
from tkinter import Tk

import numpy as np
import time

from modul6.ann import ANN
import theano.tensor as tensor
import theano.tensor.nnet as Tann
from modul4 import gamelogic as game
from modul4.gui import GameWindow
from modul4.adversial import *
from modul5.utils import rectify


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

if __name__ == '__main__':
    states, labels, scores = [], [], []
    with open('modul6/training_set.txt') as training_file:
        for line in training_file:
            data = eval(line)
            states.append(np.asarray(data[0]))
            labels.append(data[1])
            scores.append(data[2])
    ann = ANN(states, labels, scores, [300, 300, 300], [tensor.tanh, rectify, rectify, rectify, Tann.softmax], 0.001, 1, 1, 5, 'sum')
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
    while actions:
        timer = '%.2f' % (time.time() - t1)
        thing = np.array(state).flatten().tolist()
        print(thing)
        prev = state
        print("STATE: ", state)
        move = ann.predict_move(np.asarray(state).flatten().tolist())
        state = g.my_move(state, sic_dic[move])

        # app.update_view(state, score, timer)
        print(state)

        print("MOVE: ", move)

        prev_diff = np.setdiff1d(prev.reshape(-1), state.reshape(-1))
        if prev_diff.size:
            for i in prev_diff:
                score += 1 << i
        state = g.adv_move(state)

        # app.update_view(state, score, timer)

        actions = list(g.actions(state))
    print(state, timer)

    # app.update_view(state, score, 0)
    # app.game_over_screen()
    # time.sleep(3)

