import math
from random import randint
# from tkinter import Tk
import numpy as np
import time
from modul6.ann import ANN
import theano.tensor as tensor
import theano.tensor.nnet as Tann
from modul4 import gamelogic as game
# from modul4.gui import GameWindow
from modul5.utils import rectify, prelu
from modul6.ai2048demo import welch
from modul6.utils import *

La = []
Lr = []

def add_highest_tile(state, turn):
    highest_tile = max(np.asarray(state).flatten().tolist())
    if turn == 'player':
        La.append(2**highest_tile)
    elif turn == 'random':
        Lr.append(2**highest_tile)


def get_average_tile():
    return sum(La)/float(len(La))


def play_random():
    g = game._2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial

    for play in range(50):
        state = g.initial
        actions = list(g.actions(state))
        while actions:
            move = randint(0, 3)
            state = g.my_move(state, move)
            state = g.adv_move(state)
            actions = list(g.actions(state))

        print("RANDOM: ", 2**max(np.asarray(state).flatten().tolist()))
        add_highest_tile(state, "random")
    print(welch(Lr, La))

if __name__ == '__main__':
    states, labels, scores = [], [], []
    with open('modul6/wtf2.txt') as training_file:
        for line in training_file:
            data = eval(line)
            stuff = data[2]
            if stuff <= 0:
                stuff = 1
            else:
                stuff = math.log2(stuff/10)
            #print('------------')
            result = []
            for wat in data[0]:
                result.append(wat*stuff)
            #print(result)
            states.append(np.asarray(result))
            labels.append(data[1])
            scores.append(data[2])

        norms = np.apply_along_axis(np.linalg.norm, 0, np.asarray(states))
        states = (np.asarray(states) / norms).tolist()


        print(states[100])

    ann = ANN(states, labels, scores, [200], [tensor.tanh, tensor.tanh, Tann.softmax], 0.001, 50, 1, 10, 'mean')

    ann.run()

    g = game._2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial

    #root = Tk()
    #app = GameWindow(master=root)
    score = 0

    sic_dic = {0: 2, 1: 0, 2: 3, 3: 1}

    actions = list(g.actions(state))

    for play in range(50):
        state = g.initial
        actions = list(g.actions(state))
        while actions:
            prev = state

            move = ann.predict_move(np.asarray(state).flatten().tolist())
            next_move = ann.predict_next_move(np.asarray(state).flatten().tolist())

            move_two = sorted(list(next_move[0])).index(sorted(list(next_move[0]))[-2])
            move_three = sorted(list(next_move[0])).index(sorted(list(next_move[0]))[-3])
            move_four = sorted(list(next_move[0])).index(sorted(list(next_move[0]))[-4])

            current_state = np.copy(state)
            next_state = g.my_move(current_state, sic_dic[move])
            next_state_two = g.my_move(current_state, sic_dic[move_two])
            next_state_three = g.my_move(current_state, sic_dic[move_three])
            next_state_four = g.my_move(current_state, sic_dic[move_four])

            if not np.array_equal(current_state, next_state):
                state = g.my_move(state, sic_dic[move])
            elif not np.array_equal(current_state, next_state_two):
                state = g.my_move(state, sic_dic[move_two])
            elif not np.array_equal(current_state, next_state_three):
                state = g.my_move(state, sic_dic[move_three])
            else:
                state = g.my_move(state, sic_dic[move_four])

            #app.update_view(state, score, play)

            prev_diff = np.setdiff1d(prev.reshape(-1), state.reshape(-1))
            if prev_diff.size:
                for i in prev_diff:
                    score += 1 << i

            state = g.adv_move(state)
            #app.update_view(state, score, play)



            actions = list(g.actions(state))

        if (2**max(np.asarray(state).flatten().tolist()) >= 256):
            print("PLAYER: ", str(2**max(np.asarray(state).flatten().tolist())))
        else:
            print("PLAYER: ", 2**max(np.asarray(state).flatten().tolist()))
        add_highest_tile(state, "player")

    play_random()





