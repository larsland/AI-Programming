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
from scipy import stats

La = []
Lr = []


def add_highest_tile(state, turn):
    highest_tile = max(np.asarray(state).flatten().tolist())
    if turn == 'player':
        La.append(2 ** highest_tile)
    elif turn == 'adversary':
        Lr.append(2 ** highest_tile)


def get_average_tile():
    return sum(La) / float(len(La))


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

        print("RANDOM: ", 2 ** max(np.asarray(state).flatten().tolist()))
        add_highest_tile(state, "adversary")


def score_board(board):
    score = 0
    for i in board:
        score += 1 << int(i)
    return score


def merge_horizontal(state):
    mergable = [0, 0, 0, 0]
    i = 0
    for merge in range(len(mergable)):
        temp_state = state[i:i + 4]
        if temp_state:
            prev_tile = temp_state[0]
            for tile in temp_state[1::]:
                if tile == prev_tile and tile != 0:
                    mergable[merge] = 1
                    break
                prev_tile = tile
            i += 4

    return mergable


def merge_vertical(state):
    new_state = np.asarray(state)
    new_state.resize((4, 4))
    new_state = np.rot90(new_state, 1).tolist()
    return merge_horizontal(new_state)


def merge_count(state):
    return merge_horizontal(state) + merge_vertical(state)


def normalize_state(state):
    return (np.asarray(state) / max(state)).tolist()


def preprocess(state):
    new_state = list(state)
    new_state += normalize_state(list(state))
    new_state += merge_count(list(state))
    return np.asarray(state).tolist()


"""

    states, labels, scores = [], [], []
    with open('modul6/wtf.txt') as training_file:
        for line in training_file:
            state, move, score = eval(line)

            # state = list(map(lambda x: x, state))
            states.append(preprocess(state))
            labels.append(move)
            scores.append(score)

    print(len(states[0]))
    print('dlksajdkajslkdjklasjdklasjlkdjalkjsadlkj')

    ann = ANN(states, labels, scores, [300], [tensor.tanh, tensor.tanh, Tann.softmax], 0.001, 50, 1, 5, 'mean')
"""


def score_tune(state, score):
    temp_score = score
    if temp_score <= 0:
        temp_score = 1
    else:
        temp_score = math.log2(temp_score/10.)

    result = []

    for tile in state:
        result.append(tile*temp_score)

    return result


def frobeus_norm(states):
    norms = np.apply_along_axis(np.linalg.norm, 0, np.asarray(states))
    return (np.asarray(states) / norms).tolist()


def play(pre, turn):
    states, labels, scores = [], [], []
    with open('modul6/testoramalini.txt') as training_file:
        for line in training_file:
            state, move, score = eval(line)
            if pre == 0:
                states.append(np.asarray(preprocess(state)))
            else:
                states.append(np.asarray(score_tune(state, score)))

            labels.append(move)
            scores.append(score)

        states = np.asarray(frobeus_norm(states))

    ann = ANN(states, labels, scores, [300], [tensor.tanh, tensor.tanh, Tann.softmax], 0.0001, 50, 5, 'mean')
    #ann = ANN(states, labels, scores, [400, 400, 400], [rectify, rectify, rectify, rectify, Tann.softmax], 0.01, 20, 10, 'mean')


    #ann = ANN(states, labels, scores, [500, 500, 500], [tensor.tanh, tensor.tanh, tensor.tanh, tensor.tanh, Tann.softmax], 0.0001, 100, 5, 'mean')
    #ann = ANN(states, labels, scores, [500, 500, 500], [rectify, rectify, rectify, rectify, Tann.softmax], 0.0001, 100, 5, 'mean')
    #ann = ANN(states, labels, scores, [50], [tensor.tanh, tensor.tanh, Tann.softmax], 0.001, 50, 1, 'mean')

    ann.run()

    g = game._2048()
    g.initial = g.adv_move(g.initial)
    g.initial = g.adv_move(g.initial)
    state = g.initial

    move_dict = {0: 2, 1: 0, 2: 3, 3: 1}
    for play in range(50):
        score = 0
        state = g.initial
        actions = list(g.actions(state))
        while actions:
            prev = state

            temp = np.asarray(state).flatten().tolist()

            if pre == 0:
                move = ann.predict_move(preprocess(temp))
                next_move = ann.predict_next_move(preprocess(temp))
            else:
                move = ann.predict_move(temp)
                next_move = ann.predict_next_move(temp)

            move_two = sorted(list(next_move[0])).index(sorted(list(next_move[0]))[-2])
            move_three = sorted(list(next_move[0])).index(sorted(list(next_move[0]))[-3])
            move_four = sorted(list(next_move[0])).index(sorted(list(next_move[0]))[-4])

            current_state = np.copy(state)
            next_state = g.my_move(current_state, move_dict[move])
            next_state_two = g.my_move(current_state, move_dict[move_two])
            next_state_three = g.my_move(current_state, move_dict[move_three])
            next_state_four = g.my_move(current_state, move_dict[move_four])

            if not np.array_equal(current_state, next_state):
                state = g.my_move(state, move_dict[move])
            elif not np.array_equal(current_state, next_state_two):
                state = g.my_move(state, move_dict[move_two])
            elif not np.array_equal(current_state, next_state_three):
                state = g.my_move(state, move_dict[move_three])
            else:
                state = g.my_move(state, move_dict[move_four])

            # app.update_view(state, score, play)

            prev_diff = np.setdiff1d(prev.reshape(-1), state.reshape(-1))
            if prev_diff.size:
                for i in prev_diff:
                    score += 1 << i

            state = g.adv_move(state)
            # app.update_view(state, score, play)



            actions = list(g.actions(state))

        if (2 ** max(np.asarray(state).flatten().tolist()) >= 256):
            print(turn, str(2 ** max(np.asarray(state).flatten().tolist())))
        else:
            print(turn, 2 ** max(np.asarray(state).flatten().tolist()))

        add_highest_tile(state, turn)


if __name__ == '__main__':
    # root = Tk()
    # app = GameWindow(master=root)
    play(1, 'player')
    #play(0, 'adversary')

    play_random()

    print(stats.ttest_ind(Lr, La, axis=0, equal_var=False))
    print(welch(Lr, La))
